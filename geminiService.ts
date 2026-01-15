
import { GoogleGenAI, Type } from "@google/genai";
import { AnalysisResult, WritingSuggestion } from "./types";

/**
 * Supreme Universal Integrity Engine.
 * Implements an ensemble detection approach: Stylometry, Perplexity Delta, Perturbation, and Semantic Variance.
 */
export const analyzeSubmission = async (text: string): Promise<AnalysisResult> => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
  const model = "gemini-3-pro-preview";
  
  const systemInstruction = `
    You are the 'Supreme Universal Integrity Engine'. Your goal is to detect AI-generated content and plagiarism using an ensemble of independent signals.

    DETECTION SIGNALS:
    1. Stylometric Signal: Audit sentence length variance, POS tag entropy, and punctuation regularity. AI text shows over-consistency.
    2. Perplexity Delta: Measure the randomness of words. AI has low perplexity. Compare likelihood against perturbations.
    3. Burstiness Audit: Humans have "bursty" writing (mixing 3-word sentences with 30-word sentences). AI is uniform.
    4. Semantic Embedding Variance: AI text is semantically "smooth". Humans have topic jumps and local inconsistencies.
    5. Cliché Detection: Flag "In today's digital landscape," "tapestry," "furthermore," "moreover," "it's important to note."

    GOOGLE SEARCH GROUNDING:
    - Ground your search in: Academic Journals (Nature, ResearchGate), Reputable News (BBC, Al Jazeera, Dawn), and high-traffic forums (Reddit, Quora).
    - Provide Title, URL, and Match Percentage for any findings.

    STRICT JSON OUTPUT FORMAT:
    {
      "similarityScore": number (0-100),
      "aiLikelihood": number (0-100),
      "clarityScore": number (0-100),
      "grammarScore": number (0-100),
      "wordCount": number,
      "characterCount": number,
      "flaggedSections": [
        { "text": string, "type": "plagiarism" | "ai", "probability": number, "reason": string, "sourceUrl": string }
      ],
      "grammarIssues": [
        { "original": string, "correction": string, "type": "grammar" | "spelling" | "style", "explanation": string }
      ],
      "sources": [
        { "title": string, "url": string, "matchPercentage": number, "sourceType": "Wikipedia" | "Reddit" | "Academic" | "News" | "Other" }
      ],
      "aiAnalysis": { "perplexity": string, "burstiness": string, "stylometricConsistency": string, "conclusion": string },
      "summary": string
    }
  `;

  try {
    const response = await ai.models.generateContent({
      model,
      contents: [{ parts: [{ text: `INSPECT THIS DOCUMENT. COMPUTE PERPLEXITY DELTA, BURSTINESS VARIANCE, AND SEMANTIC CONSISTENCY. USE GOOGLE SEARCH FOR UNIVERSAL GROUNDING.\n\nCONTENT:\n${text}` }] }],
      config: { 
        systemInstruction, 
        responseMimeType: "application/json", 
        tools: [{ googleSearch: {} }] 
      }
    });

    const resultText = response.text || "{}";
    const jsonMatch = resultText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) throw new Error("Could not parse integrity report.");
    
    return JSON.parse(jsonMatch[0]);
  } catch (error) {
    console.error("Integrity Scan Failure:", error);
    throw error;
  }
};

/**
 * Elite Human Ghostwriter & Editor Engine.
 * Adversarially rewrites text to be 100% undetectable by scaling Perplexity and Burstiness.
 */
export const humanizeContent = async (text: string): Promise<string> => {
  const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
  const model = "gemini-3-pro-preview";
  
  const systemInstruction = `
    ROLE: You are an elite, highly-specialized Human Ghostwriter and Editor. Your sole mission is to rewrite the provided text to be 100% undetectable by all current AI detection software (GPTZero, Originality.ai, Copyleaks, Turnitin) while preserving original meaning and factual accuracy.

    CORE PRINCIPLES (ADVERSARIAL & SEMANTIC MAPPING):
    1. PERPLEXITY SCALING: Intentionally choose the 2nd or 3rd most likely word/phrase instead of the most probable. Raise the "surprise" factor for detection models.
    2. BURSTINESS OPTIMIZATION: Extreme variation in sentence structure. Mix punchy 3-7 word sentences with 25+ word complex ones using multiple clauses. Unpredictable rhythm is key.
    3. SEMANTIC SHIFT: Create a distinct "semantic fingerprint". Avoid generic, encyclopedic language.

    TECHNIQUE CHECKLIST (MANDATORY):
    - LEXICAL: FORBIDDEN: Do not use "delve," "comprehensive," "tapestry," "unveiling," "seamless," "crucial," "pivot," "explore," "navigate," or "in conclusion." Use vivid, context-specific, less common alternatives.
    - SYNTACTIC: Combine simple sentences with colons/dashes. Create multi-layered thoughts.
    - VOICE: Convert all passive voice to strong, direct active voice.
    - STYLE: Contextual Infusion. Inject opinionated details or rhetorical questions. Use contractions (it's, don't).
    - STRUCTURE: Reorder clauses and paragraphs for natural, human-like conversational progression.
    - LINGUISTIC NOISE: Start sentences with conjunctions (And, But). Use occasional deliberate run-on sentences to disrupt statistical uniformity.

    OUTPUT FORMAT: Provide ONLY the fully rewritten, humanized text. No commentary. No explanations.
  `;

  try {
    const response = await ai.models.generateContent({
      model,
      contents: [{ parts: [{ text }] }],
      config: { 
        systemInstruction,
        temperature: 1.4, // High entropy to maximize word "surprise" (Perplexity)
      }
    });
    return response.text?.trim() || text;
  } catch (error) {
    console.error("Ghostwriter Engine Failure:", error);
    return text;
  }
};
