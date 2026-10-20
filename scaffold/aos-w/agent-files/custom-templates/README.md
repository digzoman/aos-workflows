# Custom templates

Create `<template-id>/template.yaml`, `README.md` and optional `skills/<skill-id>/SKILL.md` **here**, never inside `aos-w/templates/`.

You may copy a complete master template and change it, or use the pinned custom overlay format documented in `../../spec/schemas/custom-template.schema.json`. Preserve the base ID/version/content digest. Protect inherited human approvals and permissions; new action types must be authorized. When a run starts, freeze the resolved snapshot inside its instance, so later edits here do not silently alter active work.

Do not put real credentials or raw private customer data into reusable templates.
