namespace OpenAI_DOTNET_Demo.Model
{
    public class Error
    {
        public int errorCode        { get; set; }
        public string errorMessage  { get; set; } = string.Empty;
        public string errorType     { get; set; } = string.Empty;

    }
}
