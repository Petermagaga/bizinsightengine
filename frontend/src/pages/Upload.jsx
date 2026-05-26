function Upload() {

  return (

    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        flexDirection: "column",
        background: "#f5f7fb",
      }}
    >

      <h1
        style={{
          fontSize: "36px",
          fontWeight: "700",
        }}
      >
        Upload Your Dataset
      </h1>

      <p
        style={{
          marginTop: "10px",
          color: "#6b7280",
        }}
      >
        Start by uploading a CSV
        or Excel dataset
      </p>

    </div>
  );
}

export default Upload;