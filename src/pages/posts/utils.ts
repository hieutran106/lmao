import * as fs from "node:fs";
import * as path from "node:path";

export function readAllJson() {
  console.log("Current working directory:", process.cwd());
  const posts: any[] = [];
  const folderPath = "./src/pages/posts/2024";
  const files = fs.readdirSync(folderPath);
  // Filter for JSON files and process each one
  files
    .filter((file) => path.extname(file).toLowerCase() === ".json")
    .forEach((file) => {
      const filePath = path.join(folderPath, file);
      try {
        // Read and parse the JSON file
        const fileContent = fs.readFileSync(filePath, "utf-8");
        const parsedData = JSON.parse(fileContent);

        // Add the parsed data to the array
        posts.push(parsedData);
      } catch (error) {
        console.error(`Error reading or parsing ${file}: ${error}`);
      }
    });
  return posts;
}
