'use client'

import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
  const [articles, setArticles] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchArticles() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch("http://localhost:8000/api/articles", {
          headers: {
            Authorization:
              "Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vQGRlbW8uY29tIiwiZXhwIjoxNzUxMzkzNjA4fQ.wYokyF8zuLQ96FHCJcEkm6-gJlkV0DjSF5zYbTXjvGU",
          },
        });
        if (!res.ok) throw new Error("Failed to fetch articles");
        const data = await res.json();
        setArticles(data.articles || []);
      } catch (err: any) {
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    }
    fetchArticles();
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
        <Image
          className="dark:invert"
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />

        <div className="w-full max-w-2xl mt-8">
          <h2 className="text-xl font-bold mb-4">Articles</h2>
          {loading && <div>Loading articles...</div>}
          {error && <div className="text-red-500">{error}</div>}
          {!loading && !error && (
            <ul className="space-y-4">
              {articles.length === 0 && <li>No articles found.</li>}
              {articles.map((article) => (
                <li key={article.slug} className="border rounded p-4 bg-white dark:bg-gray-900 shadow">
                  <h3 className="font-semibold text-lg mb-1">{article.title}</h3>
                  <p className="text-gray-700 dark:text-gray-300 mb-2">{article.description}</p>
                  <div className="text-xs text-gray-500">By {article.author?.username} • {new Date(article.createdAt).toLocaleDateString()}</div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/window.svg"
            alt="Window icon"
            width={16}
            height={16}
          />
          Examples
        </a>
        <a
          className="flex items-center gap-2 hover:underline hover:underline-offset-4"
          href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template-tw&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Go to nextjs.org →
        </a>
      </footer>
    </div>
  );
}
