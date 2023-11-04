/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import { useQuery } from "@tanstack/react-query";
import Card from "./Card";
import { items } from "./data";
import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";
// import { ripples } from "ldrs";
import { dotPulse } from "ldrs";

function Images({ setSelected, data, loading }) {
  console.log(loading);
  if (loading) return <div className="text-2xl text-black">loading</div>;
  return (
    <div className=" p-6 mx-4">
      <h1 className=" text-center  font-bold text-2xl mb-6">Result Images</h1>

      <ResponsiveMasonry
        columnsCountBreakPoints={{ 350: 1, 750: 2, 900: 3, 1100: 4 }}
      >
        <Masonry gutter=".5rem">
          {data?.search_results?.map((item) => {
            return <Card key={item.id} item={item} setSelected={setSelected} />;
          })}
        </Masonry>
      </ResponsiveMasonry>
    </div>
  );
}

export default Images;
