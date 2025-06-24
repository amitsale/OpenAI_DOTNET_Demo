using OpenAI_DOTNET_Demo.Model;
using OpenAI_DOTNET_Demo.Model.OpenAI.Response;

namespace OpenAI_DOTNET_Demo.Services
{
    public interface IOpenAIService
    {
        Task<OpenAIResponse> RequestCompletion(ApiRequest apirequest);
        Task<OpenAIResponse> ChatCompletion(ApiRequest apirequest);
        Task<OpenAIResponse> ChatCompletionWithTools(ApiRequest apiRequest);

        Task<string> CreateImage(ApiRequest apiRequest);
    }
}
