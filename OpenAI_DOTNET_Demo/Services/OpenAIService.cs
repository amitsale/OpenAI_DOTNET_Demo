using Microsoft.Extensions.Caching.Memory;
using Newtonsoft.Json;
using OpenAI_DOTNET_Demo.Model;
using OpenAI_DOTNET_Demo.Model.Account;
using OpenAI_DOTNET_Demo.Model.OpenAI.Response;
using OpenAI_DOTNET_Demo.Services.ServiceUtility;
using System.Collections.Generic;
using System.Net.Http.Headers;
using System.Security.Principal;
using System.Text;
using System.Text.Json;

namespace OpenAI_DOTNET_Demo.Services
{
    public class OpenAIService : IOpenAIService
    {

        HttpClient _httpClient;
        IConfiguration _configuration;
        IServiceUtility _serviceUtility;
        IWebHostEnvironment _env;

        private static readonly MemoryCache ChatSessions = new MemoryCache(new MemoryCacheOptions());
        public OpenAIService(HttpClient httpClient, IConfiguration configuration, IServiceUtility serviceUtility, IWebHostEnvironment env)
        {
            _httpClient = httpClient;
            _configuration = configuration;
            _serviceUtility = serviceUtility;
            _env = env;
        }

        public async Task<OpenAIResponse> RequestCompletion(ApiRequest apiRequest)
        {

            //Create a OpenAI Request
            var openAIRequest = _serviceUtility.CreateOpenAIRequest(apiRequest);
            //Add User Message to the OpenAI Request
            openAIRequest = _serviceUtility.AddRequestMessage(apiRequest.userQuery, openAIRequest);

            var result = await _serviceUtility.InvokeOpenApiServiceAsync(apiRequest, openAIRequest);

            return result;
        }

        public async Task<OpenAIResponse> ChatCompletion(ApiRequest apiRequest)
        {
            //Create a OpenAI Request
            var openAIRequest = _serviceUtility.CreateOpenAIRequest(apiRequest);

            List<OpenAIMessage> chatHistory = new List<OpenAIMessage>();

            //get the Chat History 
            if (apiRequest.chatSessionId != null)
            {
                ChatSessions.TryGetValue<List<OpenAIMessage>>(apiRequest.chatSessionId, out chatHistory);

            }

            if (chatHistory == null || chatHistory.Count == 0)
            {
                string newChatSessionID = Guid.NewGuid().ToString();
                chatHistory = chatHistory ?? new List<OpenAIMessage>();

                chatHistory.Add(_serviceUtility.CreateOpenAIMessage(apiRequest.userQuery, "user"));
                chatHistory.Add(_serviceUtility.CreateOpenAIMessage("You are helpful assistant.", "system"));

                //Create a new chat session and store it in memory cache
                ChatSessions.Set(newChatSessionID, chatHistory);
                //Update the apiRequest with the new chat session ID
                apiRequest.chatSessionId = newChatSessionID;
            }

            //Add New MEssage to the chat history    
            chatHistory.Add(_serviceUtility.CreateOpenAIMessage(apiRequest.userQuery, "user"));
            openAIRequest.Messages = chatHistory;

            var result = await _serviceUtility.InvokeOpenApiServiceAsync(apiRequest, openAIRequest);

            if (result != null && result?.Choices != null && result.Choices.Count > 0)
            {
                chatHistory.Add(_serviceUtility.CreateOpenAIMessage(result.Choices[0].Message.Content, result.Choices[0].Message.Role));
                result.ChatSessionId = apiRequest.chatSessionId; // Ensure the response contains the chat session ID
            }


            return result;

        }

        public async Task<OpenAIResponse> ChatCompletionWithTools(ApiRequest apiRequest)
        {
            //Create a OpenAI Request
            var openAIRequest = _serviceUtility.CreateOpenAIRequest(apiRequest);

            List<OpenAIMessage> chatHistory = new List<OpenAIMessage>();

            var tools = new List<OpenAITool>()
            {
              GetAccountToolDefinition()

            };

            openAIRequest.Tools = tools;
            openAIRequest.ToolChoice = "auto"; // Automatically choose the tool based on the request

            //get the Chat History 
            if (apiRequest.chatSessionId != null)
            {
                ChatSessions.TryGetValue<List<OpenAIMessage>>(apiRequest.chatSessionId, out chatHistory);
            }
            if (chatHistory == null || chatHistory.Count == 0)
            {
                string newChatSessionID = Guid.NewGuid().ToString();
                chatHistory = chatHistory ?? new List<OpenAIMessage>();
                chatHistory.Add(_serviceUtility.CreateOpenAIMessage(apiRequest.userQuery, "user"));
                chatHistory.Add(_serviceUtility.CreateOpenAIMessage("You are an assistant that returns account data.", "system"));
                //Create a new chat session and store it in memory cache
                ChatSessions.Set(newChatSessionID, chatHistory);
                //Update the apiRequest with the new chat session ID
                apiRequest.chatSessionId = newChatSessionID;
            }
            //Add New MEssage to the chat history    
            chatHistory.Add(_serviceUtility.CreateOpenAIMessage(apiRequest.userQuery, "user"));
            openAIRequest.Messages = chatHistory;
            var result = await _serviceUtility.InvokeOpenApiServiceAsync(apiRequest, openAIRequest);
            //Update the chat history with the response from OpenAI
            //if (result != null && result?.Choices != null && result.Choices.Count > 0)
            //{
            //    chatHistory.Add(_serviceUtility.CreateOpenAIMessage(result.Choices[0].Message.Content, result.Choices[0].Message.Role));
            //    result.ChatSessionId = apiRequest.chatSessionId; // Ensure the response contains the chat session ID
            //}


            ChatSessions.Set(apiRequest.chatSessionId, chatHistory);

            //Update the chat history with the response from OpenAI
            if (result != null && result?.Choices != null && result.Choices.Count > 0)
            {


                //var accounts = LoadAccounts();

                //var toolCall = result.Choices[0].Message.ToolCalls?.FirstOrDefault();

                //if (toolCall != null)
                //{
                //    if (toolCall?.Function?.Arguments is not null)
                //    {
                //        var argsJson = toolCall.Function.Arguments;
                //        var filter = System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, string>>(argsJson);

                //        var filteredAccounts = LoadAccounts().Where(acc =>
                //            (filter.ContainsKey("AccountNo") && acc.AccountNo == filter["AccountNo"]) ||
                //            (filter.ContainsKey("AccountName") && acc.AccountName.Contains(filter["AccountName"], StringComparison.OrdinalIgnoreCase)) ||
                //            (filter.ContainsKey("AccountType") && acc.AccountType == filter["AccountType"]) ||
                //            (filter.ContainsKey("AccountStatus") && acc.AccountStatus == filter["AccountStatus"])
                //        ).ToList();
                //    }
                //}

                var toolCall = result?.Choices?[0].Message?.ToolCalls?.FirstOrDefault();

                var accountdata = GetAccountDetails(toolCall);

                if (toolCall != null && accountdata != null && accountdata.Count > 0)
                {
                    string accountataJson = JsonConvert.SerializeObject(accountdata, Formatting.None);

                    OpenAIRequest newOpenAIRequest = _serviceUtility.CreateOpenAIRequest(apiRequest);

                    List<OpenAIMessage> newOpenAIMessages = new List<OpenAIMessage>();

                    var messageTool = new List<ToolCall>()
                    {
                        new ToolCall()
                        {
                            Id = toolCall.Id,
                            Type = "function",
                            Function = new ToolCallFunction()
                            {
                                Name = toolCall.Function.Name,
                                Description = toolCall.Function.Description,
                                Arguments = toolCall.Function.Arguments // Use the filtered account data as arguments
                            }
                        }
                    };

                    newOpenAIMessages.Add(_serviceUtility.CreateOpenAIMessage("You are an assistant that returns account data.", "system"));

                    newOpenAIMessages.Add(_serviceUtility.CreateOpenAIMessage(apiRequest.userQuery, "user"));

                    newOpenAIMessages.Add(_serviceUtility.CreateOpenAIMessage("", "assistant", messageTool));
                    newOpenAIMessages.Add(_serviceUtility.CreateOpenAIMessage(accountataJson, "tool", null, toolCall.Id));

                    newOpenAIRequest.Messages = newOpenAIMessages; // Update the OpenAI request with the new chat history

                    var finalResult = await _serviceUtility.InvokeOpenApiServiceAsync(apiRequest, newOpenAIRequest);


                    if (finalResult != null && finalResult?.Choices != null && finalResult.Choices.Count > 0)
                    {
                        result = finalResult;
                        chatHistory.Add(_serviceUtility.CreateOpenAIMessage(finalResult.Choices[0].Message.Content, finalResult.Choices[0].Message.Role));
                        ChatSessions.Set(apiRequest.chatSessionId, chatHistory);

                    }
                }
                else
                {
                    result.Choices[0].Message.Content = $"No account data found matching the criteria provided using the tool parameters .{toolCall?.Function?.Arguments ?? string.Empty}";
                }

            }

            result.ChatSessionId = apiRequest.chatSessionId; // Ensure the response contains the chat session ID
            return result;
        }

        public OpenAITool GetAccountToolDefinition()
        {
            return new OpenAITool
            {
                Function = new OpenAIToolFunction
                {
                    Name = "GetAccountDetails",
                    Description = "Return account information in structured format using filter provided by OpenAI API.",
                    Parameters = new OpenAIToolFunctionParameter
                    {
                        Properties = new Dictionary<string, object>
                {
                    { "AccountNo", new { type = "string" } },
                    { "AccountName", new { type = "string" } },
                    { "AccountMarketValue", new { type = "number" } },
                    { "AccountCash", new { type = "number" } },
                    { "AccountType", new { type = "string" } },
                    { "AccountStatus", new { type = "string" } },
                    { "AccountEQ", new { type = "number" } },
                    { "AccountFI", new { type = "number" } }
                },
                        Required = new List<string>
                        {
                            //"AccountNo", "AccountName", "AccountMarketValue", "AccountCash",
                            //"AccountType", "AccountStatus", "AccountEQ", "AccountFI"
                        }
                    }
                }
            };
        }

        public List<Account> GetAccountDetails(ToolCall toolCall)
        {
            List<Account> filterAccounts = new List<Account>();



            if (toolCall?.Function?.Arguments != null)
            {
                var args = System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, string>>(toolCall.Function.Arguments);

                // Here you mock or query real accounts
                var accounts = LoadAccounts();

                filterAccounts = accounts.Where(a =>
                    (args.ContainsKey("AccountNo") && a.AccountNo == args["AccountNo"]) ||
                    (args.ContainsKey("AccountName") && a.AccountName.Contains(args["AccountName"], StringComparison.OrdinalIgnoreCase)) ||
                    (args.ContainsKey("AccountType") && a.AccountType == args["AccountType"]) ||
                    (args.ContainsKey("AccountStatus") && a.AccountStatus == args["AccountStatus"])
                ).ToList();


            }

            return filterAccounts;
        }

        public List<Account> LoadAccounts()
        {
            var path = Path.Combine(_env.ContentRootPath, "App_Data", "mock_accounts_100.json");

            if (!File.Exists(path))
                return new List<Account>();

            var json = File.ReadAllText(path);

            return System.Text.Json.JsonSerializer.Deserialize<List<Account>>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });
        }


        public async Task<string> CreateImage(ApiRequest apiRequest)
        {
            return await _serviceUtility.InvokeOpenApiImageServiceAsync( apiRequest);
        }
    }
}