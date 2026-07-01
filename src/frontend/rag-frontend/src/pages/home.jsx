export default function Home(){ 
  return (
    <>
    <form class="class C1">
      
    <h2>Add the sources(pdfs)</h2>
    <div>
    <input
      type="file"
   onChange={(e) => {
     const file = e.target.files[0];
     console.log(file);
   }}
/>

      </div>
      </form>
    </>
  );
}
