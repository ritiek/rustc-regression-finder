#![feature(nll)]

static y: u32 = 22;
static mut x: &'static u32 = &y;

fn foo() {
    unsafe { x = &y; }
}

fn main() { }
