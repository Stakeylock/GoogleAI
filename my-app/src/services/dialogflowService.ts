export interface DialogflowResponse {
    responseText: string;
  }
  
  /**
   * Sends a message to Dialogflow CX and returns the bot response.
   * Replace the placeholders with your actual Dialogflow configuration.
   */
  export async function sendMessage(sessionId: string, message: string): Promise<DialogflowResponse> {
    const endpoint = 'https://YOUR_DIALOGFLOW_CX_ENDPOINT/v3/projects/YOUR_PROJECT/locations/YOUR_LOCATION/agents/YOUR_AGENT/sessions/' + sessionId + ':detectIntent';
    
    const payload = {
      queryInput: {
        text: {
          text: message,
        },
        languageCode: "en-US"
      }
    };
  
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer YOUR_ACCESS_TOKEN`
      },
      body: JSON.stringify(payload)
    });
  
    if (!response.ok) {
      throw new Error(`Dialogflow error: ${response.statusText}`);
    }
  
    const data = await response.json();
  
    return {
      responseText: data.queryResult?.responseMessages?.[0]?.text?.text?.[0] || "No response",
    };
  }
  