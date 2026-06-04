import {
  FileText,
  X
} from "lucide-react";

export default function ActiveDocumentBadge({

  activeDocument,

  clearDocument

}) {

  if (!activeDocument) {
    return null;
  }

  return (

    <div className="active-document-badge">

      <div className="active-document-left">

        <FileText size={16} />

        <div>

          <div className="active-document-name">

            {activeDocument.filename}

          </div>

          <div className="active-document-status">

            {

              activeDocument.status === "processing"
                ? "Analyzing document..."

                : activeDocument.status === "ready"
                ? "Ready"
                : "Upload failed"

            }

          </div>

        </div>

      </div>

      <button
        onClick={clearDocument}
        className="active-document-remove"
      >

        <X size={16} />

      </button>

    </div>

  );

}