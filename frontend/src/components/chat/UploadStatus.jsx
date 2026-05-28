import {
  Loader2
} from "lucide-react";


export default function UploadStatus({

  uploadingFiles = []

}) {

  if (
    uploadingFiles.length === 0
  ) {

    return null;
  }

  return (

    <>

      {

        uploadingFiles.map((file) => (

          <div
            key={file.id}
            className="upload-modern-card"
          >

            <Loader2
              size={16}
              className="spin"
            />

            <div>

              <div className="upload-title">

                {file.name}

              </div>

              <div className="upload-status">

                {file.status}

              </div>

            </div>

          </div>
        ))
      }

    </>
  );
}