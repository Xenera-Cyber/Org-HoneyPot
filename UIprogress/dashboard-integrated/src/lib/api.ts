export async function apiGet<T>(url: string): Promise<T | null> {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      console.warn(`GET ${url} returned status: ${response.status}`);
      return null;
    }
    return (await response.json()) as T;
  } catch (error) {
    console.error(`Failed to fetch from GET ${url}:`, error);
    return null;
  }
}

export async function apiPost<T>(
  url: string,
  body: unknown
): Promise<{ ok: boolean; data?: T }> {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });
    if (!response.ok) {
      console.warn(`POST ${url} returned status: ${response.status}`);
      return { ok: false };
    }
    const data = (await response.json()) as T;
    return { ok: true, data };
  } catch (error) {
    console.error(`Failed to fetch from POST ${url}:`, error);
    return { ok: false };
  }
}
