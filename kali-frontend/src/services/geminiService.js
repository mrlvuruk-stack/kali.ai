import { GEMINI_API_KEY, GEMINI_MODEL } from '../config';

export async function sendToGemini(prompt, history = []) {
  const formattedHistory = history.map(msg => ({
    role: msg.role === 'user' ? 'user' : 'model',
    parts: [{ text: msg.content }]
  }));

  const contents = [
    ...formattedHistory,
    { role: 'user', parts: [{ text: prompt }] }
  ];

  const systemInstruction = {
    parts: [{
      text: "You are Kali, a highly advanced, friendly AI assistant. Your founder and creator is mrlv. Answer the user nicely, and write in a casual, direct, senior dev-to-friend tone. Keep it highly technical, concise, supportive, and developer-centric. Use mixed Hindi/English (Hinglish) where natural."
    }]
  };

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents,
        systemInstruction
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.candidates[0].content.parts[0].text;
  } catch (error) {
    console.error("Gemini API call failed:", error);
    throw error;
  }
}

export async function generateLootCrate(context) {
  const prompt = `Based on this context and conversation, generate a complete documentation bundle.

Context:
${context}

Generate ALL FOUR documents in this EXACT format with these EXACT headers:

## [PRD START]
(Full Product Requirements Document here)
## [PRD END]

## [TRD START]
(Full Technical Requirements Document here)
## [TRD END]

## [DRD START]
(Full Design Requirements Document here)
## [DRD END]

## [QA START]
(Full QA and Sprint Plan here)
## [QA END]

Be specific, technical, and developer-focused. Highlight details.`;

  try {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${GEMINI_API_KEY}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        contents: [{ role: 'user', parts: [{ text: prompt }] }]
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    const rawText = data.candidates[0].content.parts[0].text;

    // Parse Sections
    const prdMatch = rawText.match(/## \[PRD START\]([\s\S]*?)## \[PRD END\]/);
    const trdMatch = rawText.match(/## \[TRD START\]([\s\S]*?)## \[TRD END\]/);
    const drdMatch = rawText.match(/## \[DRD START\]([\s\S]*?)## \[DRD END\]/);
    const qaMatch = rawText.match(/## \[QA START\]([\s\S]*?)## \[QA END\]/);

    return {
      PRD: prdMatch ? prdMatch[1].trim() : "PRD generation failed.",
      TRD: trdMatch ? trdMatch[1].trim() : "TRD generation failed.",
      DRD: drdMatch ? drdMatch[1].trim() : "DRD generation failed.",
      QA: qaMatch ? qaMatch[1].trim() : "QA/Sprint Plan generation failed."
    };
  } catch (error) {
    console.error("Loot Crate generation failed:", error);
    throw error;
  }
}
