/* eslint-disable react/prop-types */
/* eslint-disable no-unused-vars */
import { useQuery } from "@tanstack/react-query";
import Card from "./Card";
import { items } from "./data";
import Masonry, { ResponsiveMasonry } from "react-responsive-masonry";
// import { ripples } from "ldrs";
import { dotPulse } from "ldrs";

function Images({ clicked, text, setSelected }) {
  // const fetchImages = async ({ queryKey }) => {
  //   const query = queryKey[1];
  //   // console.log(query);
  //   const payload = {

  //   }
  //   const res = await fetch("https://jsonplaceholder.typicode.com/posts");

  //   return res.json();
  // };
  async function getImages() {
    const postData = {
      sites: [
        { url: "https://unsplash.com/s/photos/mammal" },
        { url: "https://unsplash.com/s/photos/animals" },

        { url: "https://unsplash.com/s/photos/cat" },
        { url: "https://unsplash.com/s/photos/dog" },
        { url: "https://unsplash.com/s/photos/savana-animals" },
        { url: "https://unsplash.com/s/photos/farm-animals" },
        { url: "https://unsplash.com/s/photos/anaconda" },
        { url: "https://unsplash.com/s/photos/amazon-animals" },
        { url: "https://unsplash.com/s/photos/amazon-animals" },
      ],
      search_text: text,
    };

    const response = await fetch("http://127.0.0.1:5000/get_images", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(postData),
    });
    return response.json();
  }

  const { data, isLoading, refetch } = useQuery({
    queryFn: getImages,
    queryKey: ["images", text],
    enabled: false,
    staleTime: Infinity,
  });

  if (clicked) {
    refetch();
  }

  dotPulse.register();



  if (isLoading) {
    return <l-dot-pulse size="43" speed="1.3" color="black"></l-dot-pulse>;

    // Default values shown

    // return (
    //   <Stack padding={4} spacing={1}>
    //     <Skeleton height="40px" isLoaded={isLoaded}>
    //       <Box>Hello World!</Box>
    //     </Skeleton>
    //     <Skeleton
    //       height="40px"
    //       isLoaded={isLoaded}
    //       bg="green.500"
    //       color="white"
    //       fadeDuration={1}
    //     >
    //       <Box>Hello React!</Box>
    //     </Skeleton>
    //     <Skeleton
    //       height="40px"
    //       isLoaded={isLoaded}
    //       fadeDuration={4}
    //       bg="blue.500"
    //       color="white"
    //     >
    //       <Box>Hello ChakraUI!</Box>
    //     </Skeleton>

    //     <Box textAlign="center">
    //       <Button onClick={() => setIsLoaded((v) => !v)}>toggle</Button>
    //     </Box>
    //   </Stack>
    // );
  }
  console.log(data);
  return (
    <div className=" p-6 mx-4">
      <h1 className=" text-center  font-bold text-2xl mb-6">Result Images</h1>
      {/* <div className=" columns-1 sm:columns-2 md:columns-3 xl:columns-4 gap-3">
        {items.map((item) => {
          return <Card key={item.id} item={item} setSelected={setSelected} />;
        })}
      </div> */}
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
