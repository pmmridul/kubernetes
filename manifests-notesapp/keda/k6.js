import http from "k6/http";
import { sleep } from "k6";
export const options = {
  vus: 400,
  duration: "120s",
};
export default function () {
  http.get("http://notesapp.local/");
  sleep(1);
}
