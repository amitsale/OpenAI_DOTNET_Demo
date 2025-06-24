using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using OpenAI_DOTNET_Demo.Model;
using OpenAI_DOTNET_Demo.Services;

namespace OpenAI_DOTNET_Demo.Controllers.OpenAI
{
    [Route("api/V1/OpenAI/")]
    [ApiController]
    public class OpenAIController : ControllerBase
    {

        public readonly IOpenAIService _openAIService;
        public IConfiguration _iConfiguration;

        public OpenAIController(IOpenAIService openAIService, IConfiguration iConfiguration)
        {
            _openAIService = openAIService;
            _iConfiguration = iConfiguration;
        }

        [HttpPost]
        [Route("Query/SimpleRequest")]
        public async Task<IActionResult> SimpleRequest(ApiRequest apiRequest)
        {
            if (string.IsNullOrWhiteSpace(apiRequest.userQuery))
            {
                return BadRequest("User query cannot be empty.");
            }
            try
            {
                var response = await _openAIService.RequestCompletion(apiRequest);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Internal server error: {ex.Message}");
            }
        }

        [HttpPost]
        [Route("Query/ChatCompletion")]
        public async Task<IActionResult> ChatCompletionRequest(ApiRequest apiRequest)
        {


            if (string.IsNullOrWhiteSpace(apiRequest.userQuery))
            {
                return BadRequest("User query cannot be empty.");
            }
            try
            {
                var response = await _openAIService.ChatCompletion(apiRequest);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Internal server error: {ex.Message}");
            }
        }

        [HttpPost]
        [Route("Query/Tools/ChatCompletion")]
        public async Task<IActionResult> ChatCompletionRequestWithAccount(ApiRequest apiRequest)
        {
            if (string.IsNullOrWhiteSpace(apiRequest.userQuery))
            {
                return BadRequest("User query cannot be empty.");
            }
            try
            {
                var response = await _openAIService.ChatCompletionWithTools(apiRequest);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Internal server error: {ex.Message}");
            }



        }


        [HttpPost]
        [Route("Command/Image/Create")]
        public async Task<IActionResult> CreateImage(ApiRequest apiRequest)
        {
            if (string.IsNullOrWhiteSpace(apiRequest.userQuery))
            {
                return BadRequest("User query cannot be empty.");
            }
            try
            {
                var response = await _openAIService.CreateImage(apiRequest);
                return Ok(response);
            }
            catch (Exception ex)
            {
                return StatusCode(StatusCodes.Status500InternalServerError, $"Internal server error: {ex.Message}");
            }




        }
    }
}
