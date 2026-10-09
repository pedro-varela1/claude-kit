---
paths:
  - "**/*.{c,h,cc,cpp,cxx,hpp,hh,cu,cuh}"
  - "**/CMakeLists.txt"
  - "**/*.cmake"
---

# C, C++ and CUDA

- C++20 (C17 for plain C). Build with CMake 3.24+ using targets only: `target_*` commands, no global
  flags. Warnings `-Wall -Wextra -Wpedantic` on, and treated as errors in CI.
- Layout: `include/<project>/` for public headers, `src/` for implementation, `apps/` for
  executables, `tests/` with CTest. One namespace per project, nested per module when it helps.
- `#pragma once`. Headers declare, sources define; include what you use.
- RAII for every resource. No raw `new`/`delete`, no owning raw pointers. Prefer `std::span`,
  `std::array`, `std::vector`, `std::unique_ptr`. `const` and `constexpr` by default, `enum class`,
  `[[nodiscard]]` on functions whose result matters.
- Errors: exceptions or `std::expected` at boundaries, chosen once per project; never ignored codes.
- Config: read `config.toml` with toml++ (header-only) into a plain `struct` per section, once, in
  `main`.
- Format with `clang-format` using the kit's `templates/.clang-format`.

## CUDA

- Kernels are small and do one thing. State the thread-to-data mapping in one comment above each
  kernel; derive grid and block sizes from config, not literals.
- Wrap every runtime call in a checking macro that reports file, line and error string.
- Keep host and device code in separate translation units where practical. Memory transfers are
  explicit and visible at the call site; prefer RAII wrappers for device buffers.
- Validate a kernel against a simple CPU reference before optimising it.
