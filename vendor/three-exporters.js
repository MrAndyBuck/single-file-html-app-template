/* THREE.STLExporter and THREE.OBJExporter for CADN'T */
( function () {

	/**
 * Usage:
 *  const exporter = new STLExporter();
 *
 *  // second argument is a list of options
 *  const data = exporter.parse( mesh, { binary: true } );
 *
 */

	class STLExporter {

		parse( scene, options = {} ) {

			const binary = options.binary !== undefined ? options.binary : false; //

			const objects = [];
			let triangles = 0;
			scene.traverse( function ( object ) {

				if ( object.isMesh ) {

					const geometry = object.geometry;

					if ( geometry.isBufferGeometry !== true ) {

						throw new Error( 'THREE.STLExporter: Geometry is not of type THREE.BufferGeometry.' );

					}

					const index = geometry.index;
					const positionAttribute = geometry.getAttribute( 'position' );
					triangles += index !== null ? index.count / 3 : positionAttribute.count / 3;
					objects.push( {
						object3d: object,
						geometry: geometry
					} );

				}

			} );
			let output;
			let offset = 80; // skip header

			if ( binary === true ) {

				const bufferLength = triangles * 2 + triangles * 3 * 4 * 4 + 80 + 4;
				const arrayBuffer = new ArrayBuffer( bufferLength );
				output = new DataView( arrayBuffer );
				output.setUint32( offset, triangles, true );
				offset += 4;

			} else {

				output = '';
				output += 'solid exported\n';

			}

			const vA = new THREE.Vector3();
			const vB = new THREE.Vector3();
			const vC = new THREE.Vector3();
			const cb = new THREE.Vector3();
			const ab = new THREE.Vector3();
			const normal = new THREE.Vector3();

			for ( let i = 0, il = objects.length; i < il; i ++ ) {

				const object = objects[ i ].object3d;
				const geometry = objects[ i ].geometry;
				const index = geometry.index;
				const positionAttribute = geometry.getAttribute( 'position' );

				if ( index !== null ) {

					// indexed geometry
					for ( let j = 0; j < index.count; j += 3 ) {

						const a = index.getX( j + 0 );
						const b = index.getX( j + 1 );
						const c = index.getX( j + 2 );
						writeFace( a, b, c, positionAttribute, object );

					}

				} else {

					// non-indexed geometry
					for ( let j = 0; j < positionAttribute.count; j += 3 ) {

						const a = j + 0;
						const b = j + 1;
						const c = j + 2;
						writeFace( a, b, c, positionAttribute, object );

					}

				}

			}

			if ( binary === false ) {

				output += 'endsolid exported\n';

			}

			return output;

			function writeFace( a, b, c, positionAttribute, object ) {

				vA.fromBufferAttribute( positionAttribute, a );
				vB.fromBufferAttribute( positionAttribute, b );
				vC.fromBufferAttribute( positionAttribute, c );

				if ( object.isSkinnedMesh === true ) {

					object.boneTransform( a, vA );
					object.boneTransform( b, vB );
					object.boneTransform( c, vC );

				}

				vA.applyMatrix4( object.matrixWorld );
				vB.applyMatrix4( object.matrixWorld );
				vC.applyMatrix4( object.matrixWorld );
				writeNormal( vA, vB, vC );
				writeVertex( vA );
				writeVertex( vB );
				writeVertex( vC );

				if ( binary === true ) {

					output.setUint16( offset, 0, true );
					offset += 2;

				} else {

					output += '\t\tendloop\n';
					output += '\tendfacet\n';

				}

			}

			function writeNormal( vA, vB, vC ) {

				cb.subVectors( vC, vB );
				ab.subVectors( vA, vB );
				cb.cross( ab ).normalize();
				normal.copy( cb ).normalize();

				if ( binary === true ) {

					output.setFloat32( offset, normal.x, true );
					offset += 4;
					output.setFloat32( offset, normal.y, true );
					offset += 4;
					output.setFloat32( offset, normal.z, true );
					offset += 4;

				} else {

					output += '\tfacet normal ' + normal.x + ' ' + normal.y + ' ' + normal.z + '\n';
					output += '\t\touter loop\n';

				}

			}

			function writeVertex( vertex ) {

				if ( binary === true ) {

					output.setFloat32( offset, vertex.x, true );
					offset += 4;
					output.setFloat32( offset, vertex.y, true );
					offset += 4;
					output.setFloat32( offset, vertex.z, true );
					offset += 4;

				} else {

					output += '\t\t\tvertex ' + vertex.x + ' ' + vertex.y + ' ' + vertex.z + '\n';

				}

			}

		}

	}

	THREE.STLExporter = STLExporter;

} )();


( function () {

	class OBJExporter {

		parse( object ) {

			let output = '';
			let indexVertex = 0;
			let indexVertexUvs = 0;
			let indexNormals = 0;
			const vertex = new THREE.Vector3();
			const color = new THREE.Color();
			const normal = new THREE.Vector3();
			const uv = new THREE.Vector2();
			const face = [];

			function parseMesh( mesh ) {

				let nbVertex = 0;
				let nbNormals = 0;
				let nbVertexUvs = 0;
				const geometry = mesh.geometry;
				const normalMatrixWorld = new THREE.Matrix3();

				if ( geometry.isBufferGeometry !== true ) {

					throw new Error( 'THREE.OBJExporter: Geometry is not of type THREE.BufferGeometry.' );

				} // shortcuts


				const vertices = geometry.getAttribute( 'position' );
				const normals = geometry.getAttribute( 'normal' );
				const uvs = geometry.getAttribute( 'uv' );
				const indices = geometry.getIndex(); // name of the mesh object

				output += 'o ' + mesh.name + '\n'; // name of the mesh material

				if ( mesh.material && mesh.material.name ) {

					output += 'usemtl ' + mesh.material.name + '\n';

				} // vertices


				if ( vertices !== undefined ) {

					for ( let i = 0, l = vertices.count; i < l; i ++, nbVertex ++ ) {

						vertex.x = vertices.getX( i );
						vertex.y = vertices.getY( i );
						vertex.z = vertices.getZ( i ); // transform the vertex to world space

						vertex.applyMatrix4( mesh.matrixWorld ); // transform the vertex to export format

						output += 'v ' + vertex.x + ' ' + vertex.y + ' ' + vertex.z + '\n';

					}

				} // uvs


				if ( uvs !== undefined ) {

					for ( let i = 0, l = uvs.count; i < l; i ++, nbVertexUvs ++ ) {

						uv.x = uvs.getX( i );
						uv.y = uvs.getY( i ); // transform the uv to export format

						output += 'vt ' + uv.x + ' ' + uv.y + '\n';

					}

				} // normals


				if ( normals !== undefined ) {

					normalMatrixWorld.getNormalMatrix( mesh.matrixWorld );

					for ( let i = 0, l = normals.count; i < l; i ++, nbNormals ++ ) {

						normal.x = normals.getX( i );
						normal.y = normals.getY( i );
						normal.z = normals.getZ( i ); // transform the normal to world space

						normal.applyMatrix3( normalMatrixWorld ).normalize(); // transform the normal to export format

						output += 'vn ' + normal.x + ' ' + normal.y + ' ' + normal.z + '\n';

					}

				} // faces


				if ( indices !== null ) {

					for ( let i = 0, l = indices.count; i < l; i += 3 ) {

						for ( let m = 0; m < 3; m ++ ) {

							const j = indices.getX( i + m ) + 1;
							face[ m ] = indexVertex + j + ( normals || uvs ? '/' + ( uvs ? indexVertexUvs + j : '' ) + ( normals ? '/' + ( indexNormals + j ) : '' ) : '' );

						} // transform the face to export format


						output += 'f ' + face.join( ' ' ) + '\n';

					}

				} else {

					for ( let i = 0, l = vertices.count; i < l; i += 3 ) {

						for ( let m = 0; m < 3; m ++ ) {

							const j = i + m + 1;
							face[ m ] = indexVertex + j + ( normals || uvs ? '/' + ( uvs ? indexVertexUvs + j : '' ) + ( normals ? '/' + ( indexNormals + j ) : '' ) : '' );

						} // transform the face to export format


						output += 'f ' + face.join( ' ' ) + '\n';

					}

				} // update index


				indexVertex += nbVertex;
				indexVertexUvs += nbVertexUvs;
				indexNormals += nbNormals;

			}

			function parseLine( line ) {

				let nbVertex = 0;
				const geometry = line.geometry;
				const type = line.type;

				if ( geometry.isBufferGeometry !== true ) {

					throw new Error( 'THREE.OBJExporter: Geometry is not of type THREE.BufferGeometry.' );

				} // shortcuts


				const vertices = geometry.getAttribute( 'position' ); // name of the line object

				output += 'o ' + line.name + '\n';

				if ( vertices !== undefined ) {

					for ( let i = 0, l = vertices.count; i < l; i ++, nbVertex ++ ) {

						vertex.x = vertices.getX( i );
						vertex.y = vertices.getY( i );
						vertex.z = vertices.getZ( i ); // transform the vertex to world space

						vertex.applyMatrix4( line.matrixWorld ); // transform the vertex to export format

						output += 'v ' + vertex.x + ' ' + vertex.y + ' ' + vertex.z + '\n';

					}

				}

				if ( type === 'Line' ) {

					output += 'l ';

					for ( let j = 1, l = vertices.count; j <= l; j ++ ) {

						output += indexVertex + j + ' ';

					}

					output += '\n';

				}

				if ( type === 'LineSegments' ) {

					for ( let j = 1, k = j + 1, l = vertices.count; j < l; j += 2, k = j + 1 ) {

						output += 'l ' + ( indexVertex + j ) + ' ' + ( indexVertex + k ) + '\n';

					}

				} // update index


				indexVertex += nbVertex;

			}

			function parsePoints( points ) {

				let nbVertex = 0;
				const geometry = points.geometry;

				if ( geometry.isBufferGeometry !== true ) {

					throw new Error( 'THREE.OBJExporter: Geometry is not of type THREE.BufferGeometry.' );

				}

				const vertices = geometry.getAttribute( 'position' );
				const colors = geometry.getAttribute( 'color' );
				output += 'o ' + points.name + '\n';

				if ( vertices !== undefined ) {

					for ( let i = 0, l = vertices.count; i < l; i ++, nbVertex ++ ) {

						vertex.fromBufferAttribute( vertices, i );
						vertex.applyMatrix4( points.matrixWorld );
						output += 'v ' + vertex.x + ' ' + vertex.y + ' ' + vertex.z;

						if ( colors !== undefined ) {

							color.fromBufferAttribute( colors, i );
							output += ' ' + color.r + ' ' + color.g + ' ' + color.b;

						}

						output += '\n';

					}

				}

				output += 'p ';

				for ( let j = 1, l = vertices.count; j <= l; j ++ ) {

					output += indexVertex + j + ' ';

				}

				output += '\n'; // update index

				indexVertex += nbVertex;

			}

			object.traverse( function ( child ) {

				if ( child.isMesh === true ) {

					parseMesh( child );

				}

				if ( child.isLine === true ) {

					parseLine( child );

				}

				if ( child.isPoints === true ) {

					parsePoints( child );

				}

			} );
			return output;

		}

	}

	THREE.OBJExporter = OBJExporter;

} )();
