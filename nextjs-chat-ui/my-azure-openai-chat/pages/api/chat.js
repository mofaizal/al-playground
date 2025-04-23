// import { OpenAIClient, AzureKeyCredential } from "@azure/openai";

// // import * as openai from "@azure/openai";

// export default async function handler(req, res) {
//   if (req.method !== 'POST') {
//     return res.status(405).json({ error: 'Method Not Allowed' });
//   }

//   const { message } = req.body;

//   if (!message) {
//     return res.status(400).json({ error: 'Message is required' });
//   }

//   const endpoint = process.env.AZURE_OPENAI_ENDPOINT;
//   const apiKey = process.env.AZURE_OPENAI_API_KEY;
//   const deploymentId = process.env.AZURE_OPENAI_DEPLOYMENT_ID || 'your-deployment-name'; // Replace with your deployment name

//   if (!endpoint || !apiKey) {
//     return res.status(500).json({ error: 'Azure OpenAI endpoint or API key not configured' });
//   }

//   const client = new OpenAIClient(endpoint, new AzureKeyCredential(apiKey));

//   try {
//     const result = await client.getChatCompletions(deploymentId, [
//       { role: "user", content: message },
//     ]);

//     const response = result.choices[0]?.message?.content || '';
//     res.status(200).json({ response });
//   } catch (error) {
//     console.error("Azure OpenAI error:", error);
//     res.status(500).json({ error: 'Failed to communicate with Azure OpenAI' });
//   }
// }

import * as openai from "@azure/openai";

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method Not Allowed' });
  }

  const { message } = req.body;

  if (!message) {
    return res.status(400).json({ error: 'Message is required' });
  }

  const endpoint = process.env.AZURE_OPENAI_ENDPOINT;
  const apiKey = process.env.AZURE_OPENAI_API_KEY;
  const deploymentId = process.env.AZURE_OPENAI_DEPLOYMENT_ID || 'your-deployment-name'; // Replace with your deployment name

  if (!endpoint || !apiKey) {
    return res.status(500).json({ error: 'Azure OpenAI endpoint or API key not configured' });
  }

  try {
    const client = new openai.OpenAIClient(endpoint, new openai.AzureKeyCredential(apiKey));
    // const client = new openai(endpoint, new openai.AzureKeyCredential(apiKey));
    const result = await client.getChatCompletions(deploymentId, [
      { role: "user", content: message },
    ]);

    const response = result.choices[0]?.message?.content || '';
    res.status(200).json({ response });
  } catch (error) {
    console.error("Azure OpenAI error:", error);
    res.status(500).json({ error: 'Failed to communicate with Azure OpenAI' });
  }
}