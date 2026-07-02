import axios from "axios";

export default function FileUpload(){

  const handleSubmit= async (e) =>{

    const file = e.target.files[0];
    if(!file) {
      console.log("File Error found");
      return ;
    };
    const url = "http://localhost:5000/upload";

    try{
      const response = await axios.post(url,file);
    }catch(error){
      console.log(error);
    }

  }; return (
    <>
      <form className="items-center justify-center bg-blue-900" onSubmit={handleSubmit}>
        <label>Upload File </label> <br/>
        <input type="file" placeholder="Choose File" /> <br/>
        <button type="submit">Upload</button>
      </form>
    </>
  );
}