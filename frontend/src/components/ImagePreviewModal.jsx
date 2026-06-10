import { X, ZoomIn, ZoomOut, Download } from "lucide-react";
import "./ImagePreviewModal.css";

export default function ImagePreviewModal({ image, onClose }) {
  if (!image) return null;

  const handleDownload = () => {
    const link = document.createElement("a");
    link.href = image.url;
    link.download = image.name || "image";
    link.click();
  };

  return (
    <div className="image-preview-overlay" onClick={onClose}>
      <div className="image-preview-modal" onClick={(e) => e.stopPropagation()}>
        <div className="image-preview-header">
          <div className="image-preview-title">
            <span>{image.name || "Image Preview"}</span>
          </div>
          <div className="image-preview-actions">
            <button className="preview-action-btn" onClick={handleDownload} title="Download">
              <Download size={18} />
            </button>
            <button className="preview-close-btn" onClick={onClose}>
              <X size={20} />
            </button>
          </div>
        </div>
        <div className="image-preview-content">
          <img src={image.url} alt={image.name || "Preview"} />
        </div>
      </div>
    </div>
  );
}