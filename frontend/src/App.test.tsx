import { fireEvent, render, screen, waitFor } from "@testing-library/react";

import { App } from "./App";

function mockFetchOnce(payload: unknown, ok = true) {
  vi.spyOn(globalThis, "fetch").mockResolvedValueOnce({
    ok,
    json: async () => payload,
  } as Response);
}

afterEach(() => {
  vi.restoreAllMocks();
});

test("renders input and analyze button", () => {
  render(<App />);
  expect(screen.getByLabelText("Contrasena")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Analizar" })).toBeInTheDocument();
});

test("shows analysis result after successful response", async () => {
  mockFetchOnce({
    score: 70,
    level: "medium",
    tokens: [{ type: "NUMBER", value: "2026" }],
    warnings: [{ code: "YEAR_DETECTED", message: "La contrasena contiene un ano reconocible." }],
    passed_rules: ["MIN_LENGTH"],
    failed_rules: ["YEAR_NOT_DETECTED"],
  });

  render(<App />);
  fireEvent.change(screen.getByLabelText("Contrasena"), { target: { value: "UTN@2026segura" } });
  fireEvent.click(screen.getByRole("button", { name: "Analizar" }));

  await waitFor(() => {
    expect(screen.getByText("70")).toBeInTheDocument();
    expect(screen.getByText("medium")).toBeInTheDocument();
    expect(screen.getByText(/YEAR_DETECTED/)).toBeInTheDocument();
  });
});

test("shows API error message", async () => {
  vi.spyOn(globalThis, "fetch").mockResolvedValueOnce({
    ok: false,
    json: async () => ({}),
  } as Response);

  render(<App />);
  fireEvent.change(screen.getByLabelText("Contrasena"), { target: { value: "bad" } });
  fireEvent.click(screen.getByRole("button", { name: "Analizar" }));

  await waitFor(() => {
    expect(screen.getByText("No se pudo analizar la contrasena. Intenta de nuevo.")).toBeInTheDocument();
  });
});

test("toggles password visibility", () => {
  render(<App />);
  const input = screen.getByLabelText("Contrasena");
  const toggle = screen.getByRole("button", { name: "Mostrar contrasena" });

  expect(input).toHaveAttribute("type", "password");
  fireEvent.click(toggle);
  expect(input).toHaveAttribute("type", "text");
});
