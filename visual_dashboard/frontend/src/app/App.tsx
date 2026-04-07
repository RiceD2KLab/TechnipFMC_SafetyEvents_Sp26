import { RouterProvider } from 'react-router';
import { router } from './routes';
import { QueryProvider } from './context/QueryContext';
import { Toaster } from './components/ui/sonner';

export default function App() {
  return (
    <QueryProvider>
      <RouterProvider router={router} />
      <Toaster />
    </QueryProvider>
  );
}
