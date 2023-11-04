import Card from "./Card";
// import { data } from "./data";
// import { data } from "./navbar";
import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";

function Images({ setSelected,data}) {
  
  return (
    <div className="p-4">
      <h1 className="text-center font-bold text-2xl mb-6">Result Images</h1>
      <ResponsiveMasonry>
        <Masonry gutter=".5rem">
        
          {
            data?.search_results.map((item) => {
              return <Card key={item.id} item={item} setSelected={setSelected} />;
            }
          )}
        </Masonry>
      </ResponsiveMasonry>
    </div>
  );
}

export default Images;
