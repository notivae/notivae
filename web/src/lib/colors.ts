export function uuidToColor(uuid: string) {
  // Simple hash function to turn UUID into a number
  let hash = 0;
  for (let i = 0; i < uuid.length; i++) {
    hash = uuid.charCodeAt(i) + ((hash << 5) - hash);
    hash = hash & hash; // Convert to 32bit integer
  }

  // Normalize hash to [0, 360) for HSL hue
  const hue = Math.abs(hash) % 360;

  // Use fixed saturation and lightness for a "friendly" look
  const saturation = 65; // %
  const lightness = 55;  // %

  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}
