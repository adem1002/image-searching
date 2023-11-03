/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import Card from "./Card";
import { items } from "./data";
import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";

function Images({ setSelected }) {
  return (
    <div className=" p-4">
      <h1 className=" text-center  font-bold text-2xl mb-6">Result Images</h1>
      {/* <div className=" columns-1 sm:columns-2 md:columns-3 xl:columns-4 gap-3">
        {items.map((item) => {
          return <Card key={item.id} item={item} setSelected={setSelected} />;
        })}
      </div> */}
      <ResponsiveMasonry>
        <Masonry gutter=".5rem">
          {items.map((item) => {
            return <Card key={item.id} item={item} setSelected={setSelected} />;
          })}
        </Masonry>
      </ResponsiveMasonry>
    </div>
  );
}

export default Images;
