import { wrap } from "svelte-spa-router/wrap";

export function protectedRoute(component) {
  return wrap({
    component,
    conditions: [
      () => {
        const token = localStorage.getItem("token");
        console.log("token", token);
        if (!token) {
          window.location.hash = "#/login";
          return false;
        }
        return true;
      },
    ],
  });
}
