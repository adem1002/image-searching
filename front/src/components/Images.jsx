/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import { useQuery } from "@tanstack/react-query";
import Card from "./Card";
import { items } from "./data";
import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";
import { tailChase } from "ldrs";

function Images({ setSelected, data, loading }) {
  console.log(data);
  tailChase.register();

  if (loading)
    return (
      <div className="flex justify-center items-center h-[90vh] ">
        <l-tail-chase size="40" speed="1.75" color="black"></l-tail-chase>
      </div>
    );
  return (
    <div className=" p-6 mx-4">
      <h1 className=" text-center  font-bold text-2xl mb-6">Result Images</h1>

      <ResponsiveMasonry
        columnsCountBreakPoints={{ 350: 1, 750: 2, 900: 3, 1100: 4 }}
      >
        {data?.search_results ? (
          <Masonry gutter=".5rem">
            {data?.search_results?.map((item) => {
              return (
                <Card key={item.id} item={item} setSelected={setSelected} />
              );
            })}
          </Masonry>
        ) : (
          <Masonry gutter=".5rem">
            {items.map((item) => {
              return (
                <Card key={item.id} item={item} setSelected={setSelected} />
              );
            })}
          </Masonry>
        )}
      </ResponsiveMasonry>
    </div>
  );
}

export default Images;
