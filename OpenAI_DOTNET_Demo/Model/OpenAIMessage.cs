using Newtonsoft.Json;

namespace OpenAI_DOTNET_Demo.Model
{
    public class OpenAIMessage
    {
        [JsonProperty("role")]
        public string Role { get; set; }

        [JsonProperty("content")]
        public string Content { get; set; }

        [JsonProperty("refusal")]
        public object Refusal { get; set; }

        [JsonProperty("annotations")]
        public List<object> Annotations { get; set; }
        [JsonProperty("tool_calls")]
        public List<ToolCall>? ToolCalls { get; set; } = null;

        [JsonProperty("tool_call_id")]
        public string? ToolCallId { get; set; }
        

    }

    public class ToolCall
    {
        [JsonProperty("id")]
        public string Id { get; set; }
        [JsonProperty("type")]
        public string Type { get; set; } // Should always be "function"
        [JsonProperty("function")]
        public ToolCallFunction Function { get; set; } 

        [JsonProperty("arguments")]
        public ToolCallFunction Arguments { get; set; }


    }

    public class ToolCallFunction
    {
        [JsonProperty("name")]
        public string Name { get; set; }
        [JsonProperty("description")]
        public string Description { get; set; }

        [JsonProperty("arguments")]
        public string Arguments { get; set; } // This is JSON string from OpenAI
    }



}
