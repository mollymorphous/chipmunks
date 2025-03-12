import { Pacifico } from "next/font/google";

const pacifico = Pacifico({
  weight: "400",
  subsets: ["latin"],
});

export default function Home() {
  return (
    <div className="flex h-dvh bg-stone-200 text-gray-900 dark:bg-neutral-800 dark:text-stone-200">
      <div className="m-auto text-center">
        <h1 className={`text-3xl ${pacifico.className}`}>Hello, Chipmunks!</h1>
      </div>
    </div>
  );
}
