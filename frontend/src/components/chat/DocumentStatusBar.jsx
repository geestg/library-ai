import {
  CheckCircle2,
  Loader2,
  AlertTriangle
} from "lucide-react";

export default function DocumentStatusBar({

  activeDocument

}) {

  if (!activeDocument) {

    return null;
  }

  const status =
    activeDocument.status ||
    "ready";

  const renderIcon = () => {

    switch (status) {

      case "processing":

        return (

          <Loader2
            size={16}
            className="spin"
          />

        );

      case "error":

        return (

          <AlertTriangle
            size={16}
          />

        );

      default:

        return (

          <CheckCircle2
            size={16}
          />

        );
    }
  };

  const renderSubtitle = () => {

    switch (status) {

      case "processing":

        return (
          "Analyzing document..."
        );

      case "error":

        return (
          "Upload failed"
        );

      default:

        return null;
    }
  };

  return (

    <div className="document-status-bar">

      <div className="document-status-icon">

        {renderIcon()}

      </div>

      <div className="document-status-content">

        <div className="document-status-name">

          {

            activeDocument.filename ||

            "Document"

          }

        </div>

        {

          renderSubtitle() && (

            <div className="document-status-subtitle">

              {renderSubtitle()}

            </div>

          )

        }

      </div>

    </div>

  );

}