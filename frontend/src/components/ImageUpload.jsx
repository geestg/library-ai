import { useState, useRef } from "react";
import { Upload, X, Image as ImageIcon, Loader2 } from "lucide-react";
import api from "../services/api";
import "./ImagePreviewModal.jsx";

export default function ImageUpload({ onImageUploaded }) {
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Create preview
    const reader = new FileReader();
    reader.onload = (ev) => {
      setPreview({
        file,
        url: ev.target.result,
        name: file.name
      });
    };
    reader.readAsDataURL(file);
    setError(null);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
      const reader = new FileReader();
      reader.onload = (ev) => {
        setPreview({
          file,
          url: ev.target.result,
          name: file.name
        });
      };
      reader.readAsDataURL(file);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!preview?.file) return;

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", preview.file);

      const response = await api.post("/upload-image", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      });

      if (response.data.status === "success") {
        // Use full URL with backend address
        const fullUrl = `http://localhost:8000${response.data.url}`;
        setPreview({
          ...preview,
          url: fullUrl,
          serverUrl: response.data.url
        });

        
        if (onImageUploaded) {
          onImageUploaded(response.data);
        }
      } else {
        setError(response.data.message || "Upload failed");
      }
    } catch (err) {
      console.error("Upload error:", err);
      setError(err.response?.data?.message || "Failed to upload image");
    } finally {
      setUploading(false);
    }
  };

  const handleClear = () => {
    setPreview(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  return (
    <div className="image-upload-container">
      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileSelect}
        style={{ display: "none" }}
      />

      {!preview ? (
        <div
          className="upload-dropzone"
          onClick={() => fileInputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
        >
          <div className="upload-icon">
            <Upload size={32} />
          </div>
          <p className="upload-text">Click or drag image here</p>
          <p className="upload-hint">Supports: JPG, PNG, GIF, WebP, BMP</p>
        </div>
      ) : (
        <div className="upload-preview">
          <img
            src={preview.url}
            alt={preview.name}
            className="preview-image"
          />
          <div className="preview-info">
            <div className="preview-name">
              <ImageIcon size={14} />
              <span>{preview.name}</span>
            </div>
            <div className="preview-actions">
              {!preview.serverUrl && (
                <button
                  onClick={handleUpload}
                  disabled={uploading}
                  className="upload-btn"
                >
                  {uploading ? (
                    <>
                      <Loader2 size={14} className="spin" />
                      Uploading...
                    </>
                  ) : (
                    <>
                      <Upload size={14} />
                      Upload
                    </>
                  )}
                </button>
              )}
              <button onClick={handleClear} className="clear-btn">
                <X size={14} />
                Clear
              </button>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="upload-error">
          {error}
        </div>
      )}
    </div>
  );
}