import { Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import RolesList from "./pages/RolesList";
import RoleDetail from "./pages/RoleDetail";
import SkillsList from "./pages/SkillsList";
import SkillDetail from "./pages/SkillDetail";
import GapReport from "./pages/GapReport";
import Bottlenecks from "./pages/Bottlenecks";
import CareerPaths from "./pages/CareerPaths";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/roles" element={<RolesList />} />
        <Route path="/roles/:roleId" element={<RoleDetail />} />
        <Route path="/skills" element={<SkillsList />} />
        <Route path="/skills/:skillId" element={<SkillDetail />} />
        <Route path="/gap-report" element={<GapReport />} />
        <Route path="/bottlenecks" element={<Bottlenecks />} />
        <Route path="/career-paths" element={<CareerPaths />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
