#!/usr/bin/env python
# -*- coding: utf-8 -*-
# r3nt0n


def count_file_lines(file_path):
    def blocks(files, size=65536):
        while True:
            b = files.read(size)
            if not b: break
            yield b

    with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
        return sum(bl.count("\n") for bl in blocks(f))
