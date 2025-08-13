<script setup lang="ts">

</script>

<template>
  <svg xmlns="http://www.w3.org/2000/svg"
       role="img"
       aria-label="Theme preview skeleton"
       viewBox="0 0 160 90"
       preserveAspectRatio="xMidYMid meet">

    <!-- Background page -->
    <rect x="0" y="0" width="160" height="90" fill="var(--background)" />

    <!-- Top header -->
    <rect x="0" y="0" width="160" height="12" rx="2" fill="var(--secondary)" />

    <!-- Header inner: left logo block + nav skeletons -->
    <g transform="translate(0, 0)">
      <rect x="3" y="2" width="14" height="8" rx="1.5" fill="var(--accent-foreground)" />
      <rect x="22" y="3.5" width="30" height="5" rx="1" fill="var(--muted-foreground)" />
      <rect x="56" y="3.5" width="18" height="5" rx="1" fill="var(--muted-foreground)" />
      <rect x="76" y="3.5" width="20" height="5" rx="1" fill="var(--muted-foreground)" />
    </g>

    <!-- Left sidebar -->
    <rect x="0" y="12" width="28" height="78" fill="var(--muted)" />
    <!-- Sidebar items -->
    <g transform="translate(3,16)">
      <rect width="22" height="6" rx="1.5" fill="var(--muted-foreground)" />
      <rect y="10" width="18" height="5" rx="1.2" fill="var(--muted-foreground)" />
      <rect y="18" width="22" height="5" rx="1.2" fill="var(--muted-foreground)" />
      <rect y="26" width="16" height="5" rx="1.2" fill="var(--muted-foreground)" />
    </g>

    <!-- Main content area -->
    <g transform="translate(32,16)">
      <!-- Card-like Border -->
      <rect x="0" y="0" width="124" height="34" rx="3" fill="var(--card)" stroke="var(--border)" stroke-width="1" />

      <!-- Hero image placeholder inside main card -->
      <rect x="4" y="4" width="54" height="26" rx="2" fill="var(--accent)" />

      <!-- Hero text skeletons -->
      <g transform="translate(62,4)">
        <rect width="58" height="6" rx="1.5" fill="var(--muted-foreground)" />
        <rect y="9" width="46" height="5" rx="1.2" fill="var(--muted-foreground)" />
      </g>

      <!-- CTA buttons in hero -->
      <g transform="translate(62,24)">
        <rect x="0" y="0" width="28" height="6" rx="1.5" fill="var(--accent-foreground)" />
        <rect x="32" y="0" width="22" height="6" rx="1.5" fill="var(--secondary)" />
      </g>
    </g>

    <!-- Lower Content -->
    <g transform="translate(32,54)">
      <!-- Lower content: list of cards / articles -->
      <g transform="translate(0,0)">
        <rect x="0" y="0" width="40" height="14" rx="2" fill="var(--card-foreground)" />
        <rect x="44" y="0" width="40" height="14" rx="2" fill="var(--card-foreground)" />
        <rect x="0" y="18" width="30" height="8" rx="1.2" fill="var(--muted-foreground)" />
        <rect x="34" y="18" width="36" height="8" rx="1.2" fill="var(--muted-foreground)" />
      </g>

      <!-- Right column small widgets -->
      <g transform="translate(88,0)">
        <rect width="36" height="10" rx="2" fill="var(--card-foreground)" />
        <rect y="12" width="36" height="6" rx="1.2" fill="var(--muted-foreground)" />
        <rect y="20" width="36" height="6" rx="1.2" fill="var(--muted-foreground)" />
      </g>
    </g>
  </svg>
</template>
