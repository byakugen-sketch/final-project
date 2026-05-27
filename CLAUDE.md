# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository

This is a general projects repository. Individual projects live in their own subdirectories.

## General Reminders

- SSH keys belong in `~/.ssh/`, never inside a project folder
- Always add a `.dockerignore` when using Docker to avoid leaking sensitive files into images
- Use `FLASK_DEBUG=true` env var rather than hardcoding `debug=True` in Flask apps
- Run `git status` before committing to check what's being staged
