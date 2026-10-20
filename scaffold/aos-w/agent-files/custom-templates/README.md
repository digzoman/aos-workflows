# Custom templates

Create `<template-id>/template.yaml`, `README.md` and optional `skills/<skill-id>/SKILL.md` **here**, never inside `aos-w/templates/`.

You may copy a complete master template and change it, or use the pinned custom overlay format documented in `../../spec/schemas/custom-template.schema.json`. Preserve the base ID/version/content digest. Protect inherited human approvals and permissions; new action types must be authorized. When a run starts, freeze the resolved snapshot inside its instance, so later edits here do not silently alter active work.

Do not put real credentials or raw private customer data into reusable templates.

## Included sanitized overlay example

`competitor-investigation-ontario/template.yaml` is a custom overlay that pins the 0.2.0 competitor-investigation source SHA-256 and changes only a regional research instruction. It cannot expand permitted actions or remove protected gates. This folder is user-owned: future framework upgrades must **preserve** it even when the base master evolves.
