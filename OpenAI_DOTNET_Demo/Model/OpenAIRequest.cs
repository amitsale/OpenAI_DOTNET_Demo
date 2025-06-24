using Newtonsoft.Json;

namespace OpenAI_DOTNET_Demo.Model
{
    public class OpenAIRequest
    {
        [JsonProperty("model")]
        public string Model { get; set; } = "gpt-4o-mini-turbo";
        
        [JsonProperty("messages")]
        public List<OpenAIMessage> Messages { get; set; } = new List<OpenAIMessage>();

        [JsonProperty("tools")]
        public List<OpenAITool>? Tools { get; set; }

        [JsonProperty("tool_choice")]
        public string? ToolChoice { get; set; } 

    }


    public class OpenAITool
    {
        [JsonProperty("id")]
        public string Id { get; set; } 
        [JsonProperty("type")]
        public string Type { get; set; } = "function";
        [JsonProperty("function")]
        public OpenAIToolFunction Function { get; set; }
    }

    public class OpenAIToolFunction
    {
        [JsonProperty("name")]
        public string Name { get; set; }

        [JsonProperty("description")]
        public string Description { get; set; } = "";

        [JsonProperty("parameters")]
        public OpenAIToolFunctionParameter Parameters { get; set; }

        [JsonProperty("arguments ")]
        public string? Arguments {get;set;}
    }


    public class OpenAIToolFunctionParameter
    {
        [JsonProperty("type")]
        public string Type { get; set; } = "object";
        [JsonProperty("properties")]
        public Dictionary<string, object> Properties { get; set; }
        [JsonProperty("required")]
        public List<string> Required { get; set; }
    }
}