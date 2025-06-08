"use client";
import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [imagePreview, setImagePreview] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0] || null;
    setFile(selectedFile);
    setResult(null);
    setError(null);

    if (selectedFile && selectedFile.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(selectedFile);
    } else {
      setImagePreview(null);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Por favor selecciona un archivo.");
      return;
    }

    const fileType = file.type;
    let payload: { pixels: number[] };

    try {
      setLoading(true);
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

<<<<<<< HEAD
      const response = await fetch("http://alb-backend-predictor-1055852265.us-east-2.elb.amazonaws.com/predict", {
=======
      const response = await fetch("alb-backend-predictor-1055852265.us-east-2.elb.amazonaws.com/predict", {
>>>>>>> 6954028526858f3aed290ad3fc94487a379ba6f6
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
    } finally {
      setLoading(false);
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
            pixels.push(gray / 255);
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
    <main className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white rounded-lg shadow-lg p-8 w-full max-w-md text-center">
        <h1 className="text-2xl font-bold mb-6 text-gray-800">
          🧠 Predicción con modelo ONNX
        </h1>

        {imagePreview && (
          <img
            src={imagePreview}
            alt="Vista previa"
            className="mb-4 rounded border shadow w-28 h-28 object-contain mx-auto"
          />
        )}

        <label
          htmlFor="fileUpload"
          className="inline-block bg-slate-700 text-white py-2 px-4 rounded cursor-pointer hover:bg-slate-600 transition"
        >
          Seleccionar archivo
        </label>

        <input
          id="fileUpload"
          type="file"
          accept=".json,image/*"
          onChange={handleFileChange}
          className="hidden"
        />

        <p className="mt-2 text-sm text-gray-600">
          {file ? `Archivo seleccionado: ${file.name}` : "Ningún archivo seleccionado"}
        </p>

        <button
          onClick={handleSubmit}
          disabled={!file || loading}
          className="mt-6 w-full py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition disabled:opacity-50 flex justify-center items-center gap-2"
        >
          {loading && (
            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          )}
          {loading ? "Procesando..." : "📤 Enviar al modelo"}
        </button>

        {result && (
          <div className="mt-6 p-4 bg-green-100 text-green-800 rounded shadow-md font-semibold">
            ✅ Predicción: {result}
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 bg-red-100 text-red-800 rounded shadow-md text-sm">
            ⚠️ {error}
          </div>
        )}
      </div>
    </main>
  );
}