#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

// Data structures
typedef struct {
    int row;
    int col;
} Point;

typedef struct {
    char** grid;
    int rows;
    int cols;
} Map;

typedef struct {
    Point* points;
    int capacity;
    int size;
} PointSet;

typedef struct {
    Point* points;
    int capacity;
    int size;
    int front;
    int back;
} PointQueue;

// Direction vectors for 4-way adjacency
const Point DIRECTIONS[4] = {
    {0, 1},   // right
    {1, 0},   // down
    {0, -1},  // left
    {-1, 0}   // up
};

// Point Set operations
PointSet* create_point_set(int initial_capacity) {
    PointSet* set = malloc(sizeof(PointSet));
    set->points = malloc(initial_capacity * sizeof(Point));
    set->capacity = initial_capacity;
    set->size = 0;
    return set;
}

bool point_equals(Point a, Point b) {
    return a.row == b.row && a.col == b.col;
}

bool point_set_contains(PointSet* set, Point p) {
    for (int i = 0; i < set->size; i++) {
        if (point_equals(set->points[i], p)) {
            return true;
        }
    }
    return false;
}

void point_set_add(PointSet* set, Point p) {
    if (!point_set_contains(set, p)) {
        if (set->size >= set->capacity) {
            set->capacity *= 2;
            set->points = realloc(set->points, set->capacity * sizeof(Point));
        }
        set->points[set->size++] = p;
    }
}

void point_set_remove(PointSet* set, Point p) {
    for (int i = 0; i < set->size; i++) {
        if (point_equals(set->points[i], p)) {
            set->points[i] = set->points[--set->size];
            return;
        }
    }
}

void free_point_set(PointSet* set) {
    free(set->points);
    free(set);
}

// Point Queue operations
PointQueue* create_point_queue(int initial_capacity) {
    PointQueue* queue = malloc(sizeof(PointQueue));
    queue->points = malloc(initial_capacity * sizeof(Point));
    queue->capacity = initial_capacity;
    queue->size = 0;
    queue->front = 0;
    queue->back = 0;
    return queue;
}

void point_queue_push(PointQueue* queue, Point p) {
    if (queue->size >= queue->capacity) {
        int new_capacity = queue->capacity * 2;
        Point* new_points = malloc(new_capacity * sizeof(Point));

        // Copy existing elements in order
        for (int i = 0; i < queue->size; i++) {
            new_points[i] = queue->points[(queue->front + i) % queue->capacity];
        }

        free(queue->points);
        queue->points = new_points;
        queue->capacity = new_capacity;
        queue->front = 0;
        queue->back = queue->size;
    }

    queue->points[queue->back] = p;
    queue->back = (queue->back + 1) % queue->capacity;
    queue->size++;
}

Point point_queue_pop(PointQueue* queue) {
    Point p = queue->points[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    queue->size--;
    return p;
}

void free_point_queue(PointQueue* queue) {
    free(queue->points);
    free(queue);
}

// Map operations
Map* create_map(int rows, int cols) {
    Map* map = malloc(sizeof(Map));
    map->rows = rows;
    map->cols = cols;
    map->grid = malloc(rows * sizeof(char*));
    for (int i = 0; i < rows; i++) {
        map->grid[i] = malloc(cols * sizeof(char));
    }
    return map;
}

void free_map(Map* map) {
    for (int i = 0; i < map->rows; i++) {
        free(map->grid[i]);
    }
    free(map->grid);
    free(map);
}

bool is_on_map(Map* map, Point p) {
    return p.row >= 0 && p.row < map->rows &&
           p.col >= 0 && p.col < map->cols;
}

// Main region walking function
PointSet* walk_region(Map* map, Point start) {
    if (!is_on_map(map, start)) {
        return NULL;
    }

    char target_char = map->grid[start.row][start.col];
    PointSet* region = create_point_set(16);
    PointSet* visited = create_point_set(16);
    PointQueue* to_visit = create_point_queue(16);

    point_set_add(region, start);
    point_set_add(visited, start);

    // Add initial neighbors
    for (int i = 0; i < 4; i++) {
        Point next = {
            start.row + DIRECTIONS[i].row,
            start.col + DIRECTIONS[i].col
        };
        if (is_on_map(map, next) && !point_set_contains(visited, next)) {
            point_queue_push(to_visit, next);
        }
    }

    // Process queue
    while (to_visit->size > 0) {
        Point current = point_queue_pop(to_visit);
        point_set_add(visited, current);

        if (map->grid[current.row][current.col] == target_char) {
            point_set_add(region, current);

            // Add unvisited neighbors
            for (int i = 0; i < 4; i++) {
                Point next = {
                    current.row + DIRECTIONS[i].row,
                    current.col + DIRECTIONS[i].col
                };
                if (is_on_map(map, next) && !point_set_contains(visited, next)) {
                    point_queue_push(to_visit, next);
                }
            }
        }
    }

    free_point_set(visited);
    free_point_queue(to_visit);

    return region;
}

// Utility function to print the region
void print_region(Map* map, PointSet* region) {
    printf("Region size: %d\n", region->size);
    printf("Points in region:\n");
    for (int i = 0; i < region->size; i++) {
        Point p = region->points[i];
        printf("(%d, %d) = '%c'\n", p.row, p.col, map->grid[p.row][p.col]);
    }
}

int main(int argc, char* argv[]) {
    // Example usage
    Map* map = create_map(3, 4);

    // Initialize example map
    const char* example_map[] = {
        "AABB",
        "AABB",
        "CCDD"
    };

    for (int i = 0; i < map->rows; i++) {
        memcpy(map->grid[i], example_map[i], map->cols);
    }

    // Walk region starting at (0,0)
    Point start = {0, 0};
    PointSet* region = walk_region(map, start);

    if (region) {
        print_region(map, region);
        free_point_set(region);
    }

    free_map(map);
    return 0;
}
