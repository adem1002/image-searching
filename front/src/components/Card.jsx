/* eslint-disable react/prop-types */
import { motion } from "framer-motion";

function Card({ item, setSelected }) {
  console.log("hello:",item?.url)
  return (
    <div
      className="h-fit relative group overflow-hidden cursor-pointer"
      onClick={() => setSelected(item)}
    >
      <motion.img
        layoutId={`card-${item.id}`}
        className="w-full z-20   "
        src={item.url}
      />

      <div className=" transition-all duration-300 group-hover:bottom-0  group-hover:opacity-100 flex absolute -bottom-32  w-full h-full  bg-black/50  opacity-0 justify-center items-center">
        <p className="text-white">{item.title}</p>
      </div>
    </div>
  );
}

export default Card;
