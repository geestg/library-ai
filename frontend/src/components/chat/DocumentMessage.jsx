import {
  FileText,
  Loader2,
  CheckCircle2,
  AlertCircle
} from "lucide-react";

export default function DocumentMessage({

  document

}) {

  if (!document) {
    return null;
  }

  const renderStatusIcon = () => {

    switch (
      document.status
    ) {

      case "processing":

        return (

          <Loader2
            size={16}
            className="spin"
          />

        );

      case "ready":

        return (

          <CheckCircle2
            size={16}
          />

        );

      case "error":

        return (

          <AlertCircle
            size={16}
          />

        );

      default:

        return null;
    }
  };

  const renderStatusText = () => {

    switch (
      document.status
    ) {

      case "processing":
        return "Analyzing document...";

      case "ready":
        return "Ready";

      case "error":
        return "Upload failed";

      default:
        return "";
    }
  };

  return (

    <div className="document-message-card">

      <div className="document-message-icon">

        <FileText size={18} />

      </div>

      <div className="document-message-content">

        <div className="document-message-name">

          {document.filename}

        </div>

        <div className="document-message-status">

          {renderStatusIcon()}

          {renderStatusText()}

        </div>

      </div>

    </div>

  );
}