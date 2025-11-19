#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sorting algorithm visualizer.
Creates animated visualizations for sorting algorithms.
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import List, Tuple, Callable
import numpy as np


class SortingVisualizer:
    """Visualize sorting algorithms step by step."""

    def __init__(self, algorithm_name: str, data: List[int]):
        """
        Initialize visualizer.

        Args:
            algorithm_name: Name of the sorting algorithm
            data: List of integers to sort
        """
        self.algorithm_name = algorithm_name
        self.data = data.copy()
        self.steps = []
        self.comparisons = 0
        self.swaps = 0

    def record_step(self, arr: List[int], highlights: List[int] = None):
        """
        Record a step in the sorting process.

        Args:
            arr: Current state of array
            highlights: Indices to highlight (e.g., elements being compared)
        """
        self.steps.append({"array": arr.copy(), "highlights": highlights or []})

    def visualize_bubble_sort(self) -> animation.FuncAnimation:
        """Visualize bubble sort algorithm."""
        arr = self.data.copy()
        n = len(arr)

        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                self.comparisons += 1
                self.record_step(arr, [j, j + 1])

                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps += 1
                    swapped = True
                    self.record_step(arr, [j, j + 1])

            if not swapped:
                break

        return self._create_animation()

    def visualize_quick_sort(self) -> animation.FuncAnimation:
        """Visualize quick sort algorithm."""
        arr = self.data.copy()

        def partition(low: int, high: int) -> int:
            pivot = arr[high]
            i = low - 1

            for j in range(low, high):
                self.comparisons += 1
                self.record_step(arr, [j, high])

                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    if i != j:
                        self.swaps += 1
                        self.record_step(arr, [i, j])

            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            self.swaps += 1
            self.record_step(arr, [i + 1, high])
            return i + 1

        def quick_sort(low: int, high: int):
            if low < high:
                pi = partition(low, high)
                quick_sort(low, pi - 1)
                quick_sort(pi + 1, high)

        quick_sort(0, len(arr) - 1)
        return self._create_animation()

    def visualize_merge_sort(self) -> animation.FuncAnimation:
        """Visualize merge sort algorithm."""
        arr = self.data.copy()

        def merge(left: int, mid: int, right: int):
            left_arr = arr[left : mid + 1]
            right_arr = arr[mid + 1 : right + 1]

            i = j = 0
            k = left

            while i < len(left_arr) and j < len(right_arr):
                self.comparisons += 1
                self.record_step(arr, [left + i, mid + 1 + j])

                if left_arr[i] <= right_arr[j]:
                    arr[k] = left_arr[i]
                    i += 1
                else:
                    arr[k] = right_arr[j]
                    j += 1
                k += 1
                self.record_step(arr, [k - 1])

            while i < len(left_arr):
                arr[k] = left_arr[i]
                i += 1
                k += 1
                self.record_step(arr, [k - 1])

            while j < len(right_arr):
                arr[k] = right_arr[j]
                j += 1
                k += 1
                self.record_step(arr, [k - 1])

        def merge_sort(left: int, right: int):
            if left < right:
                mid = (left + right) // 2
                merge_sort(left, mid)
                merge_sort(mid + 1, right)
                merge(left, mid, right)

        merge_sort(0, len(arr) - 1)
        return self._create_animation()

    def _create_animation(self) -> animation.FuncAnimation:
        """Create matplotlib animation from recorded steps."""
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_title(
            f"{self.algorithm_name} - Comparisons: {self.comparisons}, Swaps: {self.swaps}"
        )
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")

        bars = ax.bar(range(len(self.data)), self.data, color="skyblue")

        def animate(frame):
            if frame < len(self.steps):
                step = self.steps[frame]
                arr = step["array"]
                highlights = step.get("highlights", [])

                for i, (bar, val) in enumerate(zip(bars, arr)):
                    bar.set_height(val)
                    if i in highlights:
                        bar.set_color("red")
                    else:
                        bar.set_color("skyblue")

                ax.set_title(
                    f"{self.algorithm_name} - Step {frame + 1}/{len(self.steps)}"
                )

            return bars

        anim = animation.FuncAnimation(
            fig, animate, frames=len(self.steps), interval=100, repeat=False, blit=False
        )

        return anim

    def save_animation(self, filename: str, fps: int = 10):
        """Save animation to file."""
        anim = self._create_animation()
        anim.save(filename, writer="pillow", fps=fps)
        plt.close()


def visualize_sorting_algorithm(
    algorithm_name: str, data: List[int], output_file: str = None
):
    """
    Visualize a sorting algorithm.

    Args:
        algorithm_name: Name of algorithm ('bubble', 'quick', 'merge')
        data: Data to sort
        output_file: Optional file to save animation
    """
    visualizer = SortingVisualizer(algorithm_name, data)

    if algorithm_name.lower() == "bubble":
        anim = visualizer.visualize_bubble_sort()
    elif algorithm_name.lower() == "quick":
        anim = visualizer.visualize_quick_sort()
    elif algorithm_name.lower() == "merge":
        anim = visualizer.visualize_merge_sort()
    else:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")

    if output_file:
        visualizer.save_animation(output_file)
    else:
        plt.show()

    return visualizer


if __name__ == "__main__":
    # Example usage
    data = [64, 34, 25, 12, 22, 11, 90, 5]
    visualize_sorting_algorithm("bubble", data, "bubble_sort.gif")
