import { createBrowserRouter, createRoutesFromElements, Route, RouterProvider} from "react-router-dom"
import Home from "./pages/Home";
import { ThemeProvider } from "@mui/material";
import { createMuiTheme } from "./theme/theme";
import Explore from "./pages/Explore";

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route>
      <Route path="/" element={<Home />} />
      <Route path="/explore/:categoryName" element={<Explore />} />

    </Route>
    
  )
);

const App: React.FC = () => {
  const theme = createMuiTheme();
  return (
    <ThemeProvider theme={theme}>
      <RouterProvider router={router}/>
    </ThemeProvider>
  );
  
};

export default App;
