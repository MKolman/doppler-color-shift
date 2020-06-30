/* tslint:disable */
/* eslint-disable */
/**
* Given an HTML Canvas context it will transform its image in place into what it
* would look like if they were moving at `velocity` relative to the observer.
*
* `velocity` is measured in speed of light and can be in
* range (-1, 1) -- non-inclusively on both sides
* @param {CanvasRenderingContext2D} ctx
* @param {number} velocity
*/
export function color_shift_canvas(ctx: CanvasRenderingContext2D, velocity: number): void;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly color_shift_canvas: (a: number, b: number) => void;
  readonly __wbindgen_malloc: (a: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number) => number;
  readonly __wbindgen_exn_store: (a: number) => void;
}

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {InitInput | Promise<InitInput>} module_or_path
*
* @returns {Promise<InitOutput>}
*/
export default function init (module_or_path?: InitInput | Promise<InitInput>): Promise<InitOutput>;
        