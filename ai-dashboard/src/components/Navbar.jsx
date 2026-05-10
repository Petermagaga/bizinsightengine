export default function Navbar() {
  return (
    <div className="bg-white border-b px-6 py-4 flex justify-between items-center">

      <h1 className="text-2xl font-semibold">
        Dashboard
      </h1>

      <div className="flex items-center gap-4">

        <input
          placeholder="Search..."
          className="border rounded-lg px-4 py-2"
        />

        <div className="w-10 h-10 rounded-full bg-blue-500 text-white flex items-center justify-center">
          U
        </div>

      </div>

    </div>
  );
}