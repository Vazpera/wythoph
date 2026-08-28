use pyo3::prelude::*;

#[derive(Debug)]
#[pyclass]
struct MeshData {
    #[pyo3(get)]
    vertices: Vec<(f32, f32, f32)>,
    #[pyo3(get)]
    faces: Vec<Vec<usize>>,
}


#[pyfunction]
#[pyo3(signature = (numerators, denominators, ringing))] // Add this line!
fn generate_cube_geometry(numerators: Vec<i32>, denominators: Vec<i32>, ringing: Vec<f32>) -> PyResult<MeshData> {
    let half = 4 as f32 / 2.0;

    let vertices = vec![
        (-half, -half, -half), 
        ( half, -half, -half), 
        ( half,  half, -half), 
        (-half,  half, -half), 
        (-half, -half,  half), 
        ( half, -half,  half), 
        ( half,  half,  half), 
        (-half,  half,  half), 
    ];

    let faces = vec![
        vec![0, 1, 2, 3], 
        vec![4, 5, 6, 7], 
        vec![0, 1, 5, 4], 
        vec![1, 2, 6, 5], 
        vec![2, 3, 7, 6], 
        vec![3, 0, 4, 7], 
    ];

    Ok(MeshData { vertices, faces })
}

#[pymodule]
fn rust_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<MeshData>()?;
    m.add_function(wrap_pyfunction!(generate_cube_geometry, m)?)?;
    Ok(())
}
