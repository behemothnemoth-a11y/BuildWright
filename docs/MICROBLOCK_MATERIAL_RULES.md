# Microblock Material Rules

1. Preserve the vanilla material story.
2. Validate every requested cell material against the active provider.
3. Use microblocks as shape tools first; avoid confetti palettes inside one host.
4. Preserve directional states where supported.
5. Keep behavior-sensitive blocks vanilla.
6. Unsupported glass/fluid/animated/tinted/functional behavior defaults to vanilla.
7. Material inlay is ornament; it should not become noise texture.

The provider profile deliberately stores a snapshot count, not a duplicated material whitelist. Astra's own material library remains authoritative.
