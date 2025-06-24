using Newtonsoft.Json;
using System.Collections.Generic;

namespace OpenAI_DOTNET_Demo.Model.OpenAI.Response
{
    public class OpenAIResponse
    {
        [JsonProperty("id")]
        public string Id { get; set; }

        [JsonProperty("object")]
        public string Object { get; set; }

        [JsonProperty("created")]
        public long Created { get; set; }

        [JsonProperty("model")]
        public string Model { get; set; }

        [JsonProperty("choices")]
        public List<OpenAIChoice> Choices { get; set; }

        [JsonProperty("usage")]
        public OpenAIUsage Usage { get; set; }

        [JsonProperty("service_tier")]
        public string ServiceTier { get; set; }

        [JsonProperty("system_fingerprint")]
        public string SystemFingerprint { get; set; }

        public string? ChatSessionId { get; set; }
            
      
    }

    public class OpenAIChoice
    {
        [JsonProperty("index")]
        public int Index { get; set; }

        [JsonProperty("message")]
        public OpenAIMessage Message { get; set; }

        [JsonProperty("logprobs")]
        public object Logprobs { get; set; }

        [JsonProperty("finish_reason")]
        public string FinishReason { get; set; }
    }

   

    public class OpenAIUsage
    {
        [JsonProperty("prompt_tokens")]
        public int PromptTokens { get; set; }

        [JsonProperty("completion_tokens")]
        public int CompletionTokens { get; set; }

        [JsonProperty("total_tokens")]
        public int TotalTokens { get; set; }

        [JsonProperty("prompt_tokens_details")]
        public PromptTokensDetails PromptTokensDetails { get; set; }

        [JsonProperty("completion_tokens_details")]
        public CompletionTokensDetails CompletionTokensDetails { get; set; }
    }

    public class PromptTokensDetails
    {
        [JsonProperty("cached_tokens")]
        public int CachedTokens { get; set; }

        [JsonProperty("audio_tokens")]
        public int AudioTokens { get; set; }
    }

    public class CompletionTokensDetails
    {
        [JsonProperty("reasoning_tokens")]
        public int ReasoningTokens { get; set; }

        [JsonProperty("audio_tokens")]
        public int AudioTokens { get; set; }

        [JsonProperty("accepted_prediction_tokens")]
        public int AcceptedPredictionTokens { get; set; }

        [JsonProperty("rejected_prediction_tokens")]
        public int RejectedPredictionTokens { get; set; }
    }


}
