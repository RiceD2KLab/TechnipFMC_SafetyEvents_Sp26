import { RouterProvider } from 'react-router';
import { router } from './routes';
import { QueryProvider } from './context/QueryContext';

export default function App() {
  return (
    <QueryProvider>
      <RouterProvider router={router} />
    </QueryProvider>
  );
}
