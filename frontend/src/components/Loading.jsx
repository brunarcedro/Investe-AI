export default function Loading({ message = "Carregando..." }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-primary"></div>
      <p className="mt-4 text-gray-600 font-medium">{message}</p>
    </div>
  );
}
