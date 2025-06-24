using Newtonsoft.Json;
using OpenAI_DOTNET_Demo.Model;
using OpenAI_DOTNET_Demo.Model.OpenAI.Response;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;

namespace OpenAI_DOTNET_Demo.Services.ServiceUtility
{
    public interface IServiceUtility
    {
         public string GetOpenApiKey(IConfiguration configuration);
         public string GetOpenApiUrl(IConfiguration configuration); 
         public OpenAIRequest AddRequestMessage(string userQuery, OpenAIRequest openAIRequest, string role = "user");
         
        public OpenAIMessage CreateOpenAIMessage(string content, string role = "user" , List<ToolCall>? toolCall = null , string? tool_call_id= null);

        public Task<OpenAIResponse> InvokeOpenApiServiceAsync(ApiRequest apiRequest, OpenAIRequest openAIRequest);
        public OpenAIRequest CreateOpenAIRequest(ApiRequest apiRequest, string model = "gpt-3.5-turbo", double temp = 0.3, int maxToken = 1000);
        public Task<string> InvokeOpenApiImageServiceAsync(ApiRequest apiRequestt);

    }
}
