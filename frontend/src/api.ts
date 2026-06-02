export type Token = {
  type: string;
  value: string;
};

export type WarningItem = {
  code: string;
  message: string;
};

export type AnalyzePasswordResponse = {
  score: number;
  level: "weak" | "medium" | "strong";
  tokens: Token[];
  warnings: WarningItem[];
  passed_rules: string[];
  failed_rules: string[];
};

export async function analyzePassword(password: string): Promise<AnalyzePasswordResponse> {
  const response = await fetch("/password/analyze", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ password }),
  });

  if (!response.ok) {
    throw new Error("No se pudo analizar la contrasena.");
  }

  return (await response.json()) as AnalyzePasswordResponse;
}
