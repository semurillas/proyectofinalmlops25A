"use client";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
    setResult(null);
    setError(null);
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Por favor selecciona un archivo.");
      return;
    }

    const fileType = file.type;
    let payload: { pixels: number[] };

    try {
      if (fileType === "application/json") {
        const text = await file.text();
        const json = JSON.parse(text);
        if (!json.pixels || !Array.isArray(json.pixels)) {
          throw new Error("JSON inválido: falta el campo 'pixels'");
        }
        payload = { pixels: json.pixels };
      } else if (fileType.startsWith("image/")) {
        const pixels = await imageTo28x28GrayPixels(file);
        payload = { pixels };
      } else {
        setError("Archivo no compatible. Usa .json o imagen (.jpg, .png).");
        return;
      }

      const response = await fetch("http://18.118.208.57:8001/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error("Error al procesar la predicción.");
      }

      const data = await response.json();
      setResult(data.prediccion?.toString() || "Sin resultado");
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Error desconocido";
      console.error("Error:", err);
      setError(errorMessage);
      setResult(null);      
    }
  };

  const imageTo28x28GrayPixels = (file: File): Promise<number[]> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = function (e) {
        const img = new Image();
        img.onload = function () {
          const canvas = document.createElement("canvas");
          const ctx = canvas.getContext("2d");
          if (!ctx) return reject("No se pudo crear el contexto del canvas");

          canvas.width = 28;
          canvas.height = 28;

          ctx.drawImage(img, 0, 0, 28, 28);
          const imageData = ctx.getImageData(0, 0, 28, 28).data;

          const pixels: number[] = [];
          for (let i = 0; i < imageData.length; i += 4) {
            const gray = (imageData[i] + imageData[i + 1] + imageData[i + 2]) / 3;
            pixels.push(gray / 255); // Normalizar
          }

          resolve(pixels);
        };

        img.onerror = reject;
        img.src = e.target?.result as string;
      };

      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-gray-100">
      <h1 className="text-2xl font-bold mb-4 text-center">Predicción con modelo ONNX</h1>

      <input
        type="file"
        accept=".json,image/*"
        onChange={handleFileChange}
        className="mb-4"
      />

      <button
        onClick={handleSubmit}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Enviar al modelo
      </button>

      {result && (
        <div className="mt-4 p-3 bg-green-100 text-green-800 rounded">
          Predicción: {result}
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
          Error: {error}
        </div>
      )}
    </main>
  );
}
