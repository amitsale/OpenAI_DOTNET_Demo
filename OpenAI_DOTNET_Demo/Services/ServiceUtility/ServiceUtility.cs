using Microsoft.AspNetCore.DataProtection.KeyManagement;
using Newtonsoft.Json; 
using OpenAI_DOTNET_Demo.Model;
using OpenAI_DOTNET_Demo.Model.OpenAI.Response;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Reflection.Metadata.Ecma335;
using System.Text;
using System.Text.Json;

namespace OpenAI_DOTNET_Demo.Services.ServiceUtility
{
    public class ServiceUtility : IServiceUtility
    {
        private readonly IConfiguration _configuration;
        private readonly string _openApiKey;
        private readonly string _openApiUrl;

        public ServiceUtility(IConfiguration configuration)
        {
            _configuration = configuration;
            _openApiKey = GetOpenApiKey(configuration);
            _openApiUrl = GetOpenApiUrl(configuration);
        }

        public string GetOpenApiKey(IConfiguration configuration)
        {
            var apiKey = configuration["OpenAI:ApiKey"];
            if (string.IsNullOrEmpty(apiKey))
            {
                throw new ArgumentException("API key is not configured.");
            }
            return apiKey;
        }

        public string GetOpenApiUrl(IConfiguration configuration)
        {
            var apiUrl = configuration["OpenAI:ApiUrl"];
            if (string.IsNullOrEmpty(apiUrl))
            {
                throw new ArgumentException("API URL is not configured.");
            }
            return apiUrl;
        }

        public OpenAIMessage CreateOpenAIMessage(string content, string role = "user" , List<ToolCall>? toolCalls = null, string? tool_call_id = null)
        {
            return new OpenAIMessage()
            {
                Role = role
                 ,
                Content = content
                ,
                ToolCalls = toolCalls

                , ToolCallId = tool_call_id
            };
        }

        public OpenAIRequest CreateOpenAIRequest(ApiRequest apiRequest,string model = "gpt-3.5-turbo" , double temp = 0.3, int maxToken = 1000) 
        {
            if (apiRequest == null || string.IsNullOrWhiteSpace(apiRequest.userQuery))
            {
                throw new ArgumentException("Invalid API request. User query cannot be empty.");
            }
            return new OpenAIRequest
            {
                Model = model, // or any other model you want to use
                
                //,
                //MaxTokens = 100, // Adjust as needed
                //Temperature = 0.7f // Adjust as needed
            };

        }

        public OpenAIRequest AddRequestMessage(string userQuery, OpenAIRequest openAIRequest, string role = "user")
        {
            if (string.IsNullOrWhiteSpace(userQuery))
            {
                throw new ArgumentException("User query cannot be empty.");
            }
            openAIRequest.Messages.Add(new OpenAIMessage
            {
                Role = role,
                Content = userQuery
            });
            return openAIRequest;
        }
        public async Task<OpenAIResponse> InvokeOpenApiServiceAsync(ApiRequest apiRequest, OpenAIRequest openAIRequest)
        {
            var apiResponse = new OpenAIResponse();

            try
            {
                using (var httpClient = new HttpClient())
                {
                    httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _openApiKey);

                    var content = new StringContent(JsonConvert.SerializeObject(openAIRequest), Encoding.UTF8, "application/json");
                    var response = await httpClient.PostAsync(_openApiUrl, content);
                    var result = await response.Content.ReadAsStringAsync();

                    if (!response.IsSuccessStatusCode)
                    {
                        throw new HttpRequestException($"Error calling OpenAI API: {response.StatusCode} - {result}");
                    }
                    else
                    {
                        var chatResponse = JsonConvert.DeserializeObject<OpenAIResponse>(result);

                        apiResponse = chatResponse ?? new OpenAIResponse
                        {
                            Choices = new List<OpenAIChoice>
                            {
                                new OpenAIChoice
                                {
                                    Message = new OpenAIMessage { Role = "assistant", Content = "No response received." }
                                }
                            }
                        };
                    }

                }

                return apiResponse;
            }
            catch (Exception Ex)
            {

                throw new Exception($"An error occurred while invoking the OpenAI API: {Ex.Message}", Ex);
            }
        }

        public async Task<string> InvokeOpenApiImageServiceAsync(ApiRequest apiRequest)
        {
            var apiResponse = new OpenAIResponse();

            try
            {
                using (var httpClient = new HttpClient())
                {
                    //httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _openApiKey);

                    //var content = new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json");
                    //var response = await httpClient.PostAsync(_openApiUrl, content);
                    //var result = await response.Content.ReadAsStringAsync();

                    //if (!response.IsSuccessStatusCode)
                    //{
                    //    throw new HttpRequestException($"Error calling OpenAI API: {response.StatusCode} - {result}");
                    //}
                    //else
                    //{
                    //    var chatResponse = JsonConvert.DeserializeObject<OpenAIResponse>(result);

                    //    apiResponse = chatResponse ?? new OpenAIResponse
                    //    {
                    //        Choices = new List<OpenAIChoice>
                    //        {
                    //            new OpenAIChoice
                    //            {
                    //                Message = new OpenAIMessage { Role = "assistant", Content = "No response received." }
                    //            }
                    //        }
                    //    };
                    //}

                    var requestUrl = "https://api.openai.com/v1/images/generations";

                    var requestBody = new
                    {
                        prompt = apiRequest.userQuery,
                        n = 1,
                        size = "512x512" // or "256x256", "1024x1024"
                    };

                    httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", _openApiKey);

                    var jsonContent = new StringContent(JsonConvert.SerializeObject(requestBody), Encoding.UTF8, "application/json"); 

                    var response = await httpClient.PostAsync(requestUrl, jsonContent);
                    response.EnsureSuccessStatusCode();

                    var responseString = await response.Content.ReadAsStringAsync();

                    using var doc = JsonDocument.Parse(responseString);
                    var imageUrl = doc.RootElement
                        .GetProperty("data")[0]
                        .GetProperty("url")
                        .GetString();

                    return imageUrl;

                } 
            }
            catch (Exception Ex)
            {

                throw new Exception($"An error occurred while invoking the OpenAI API: {Ex.Message}", Ex);
            }


        }
    }
}
